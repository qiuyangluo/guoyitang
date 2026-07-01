/**
 * POST /api/calendar-event
 * Creates an event on the clinic Google Calendar using GOOGLE_SERVICE_ACCOUNT_JSON.
 *
 * Env:
 *   GOOGLE_SERVICE_ACCOUNT_JSON — full service account JSON (Vercel env var)
 *   GOOGLE_CALENDAR_ID — optional; defaults to Guoyitang group calendar
 *   CALENDAR_ALLOWED_ORIGINS — comma-separated; default guoyitangus.com + localhost
 *   CALENDAR_INGEST_SECRET — optional; if set, require Authorization: Bearer <secret>
 *   EVENT_DEFAULT_LOCATION — optional address string
 *   APPOINTMENT_NOTIFICATION_EMAILS — optional comma-separated notification emails
 *   RESEND_API_KEY / RESEND_FROM — optional Resend email sender config
 *   SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASS — optional email sender config
 *   SMTP_FROM — optional sender; defaults to SMTP_USER
 */

const { google } = require("googleapis");
const nodemailer = require("nodemailer");

const DEFAULT_CALENDAR_ID =
  process.env.GOOGLE_CALENDAR_ID ||
  "ef8853dedc6ed1d1ece86143cdf92565df582916b9098a7892b09b75b959bdef@group.calendar.google.com";

const DEFAULT_LOCATION =
  process.env.EVENT_DEFAULT_LOCATION ||
  "142-38 37th Ave #1C1D, Flushing, NY 11354";

const DEFAULT_NOTIFICATION_EMAILS =
  process.env.APPOINTMENT_NOTIFICATION_EMAILS ||
  "jbj899@yahoo.com,guoyitang11366@gmail.com";

const MAX_BODY = 48 * 1024;

function parseCredentials() {
  const raw = process.env.GOOGLE_SERVICE_ACCOUNT_JSON;
  if (!raw || !String(raw).trim()) return null;
  let creds;
  try {
    creds = JSON.parse(raw);
  } catch {
    throw new Error("INVALID_JSON");
  }
  if (creds.private_key && typeof creds.private_key === "string") {
    creds.private_key = creds.private_key.replace(/\\n/g, "\n");
  }
  return creds;
}

function corsHeaders(req, res) {
  const list = (
    process.env.CALENDAR_ALLOWED_ORIGINS ||
    "https://guoyitangus.com,https://www.guoyitangus.com,http://localhost:3000"
  )
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  const origin = req.headers.origin;
  if (origin && list.includes(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
    res.setHeader("Vary", "Origin");
  }
}

/** Vercel / some hosts parse JSON before invoking the handler. */
async function resolveJsonBody(req) {
  if (req.body != null && typeof req.body !== "undefined") {
    if (typeof req.body === "string") {
      try {
        return req.body ? JSON.parse(req.body) : {};
      } catch {
        throw new Error("INVALID_JSON_BODY");
      }
    }
    if (typeof req.body === "object") return req.body;
  }
  return readJsonBody(req);
}

function readJsonBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    let len = 0;
    req.on("data", (chunk) => {
      len += chunk.length;
      if (len > MAX_BODY) {
        reject(new Error("BODY_TOO_LARGE"));
        req.destroy();
        return;
      }
      data += chunk;
    });
    req.on("end", () => {
      try {
        resolve(data ? JSON.parse(data) : {});
      } catch {
        reject(new Error("INVALID_JSON_BODY"));
      }
    });
    req.on("error", reject);
  });
}

function trimStr(v, max) {
  if (v == null) return "";
  const s = String(v).trim();
  return max ? s.slice(0, max) : s;
}

function notificationEmails() {
  return DEFAULT_NOTIFICATION_EMAILS.split(",")
    .map((email) => trimStr(email, 320))
    .filter(Boolean);
}

function calendarErrorCode(err) {
  return err.code || err.response?.status;
}

function smtpConfig() {
  const host = trimStr(process.env.SMTP_HOST);
  const user = trimStr(process.env.SMTP_USER);
  const pass = trimStr(process.env.SMTP_PASS);
  if (!host || !user || !pass) return null;
  const port = parseInt(process.env.SMTP_PORT || "", 10);
  return {
    host,
    port: Number.isFinite(port) ? port : 465,
    secure: String(process.env.SMTP_SECURE || "true").toLowerCase() !== "false",
    auth: { user, pass },
    from: trimStr(process.env.SMTP_FROM, 320) || user,
  };
}

async function sendWithResend({ to, subject, text }) {
  const apiKey = trimStr(process.env.RESEND_API_KEY);
  const from = trimStr(process.env.RESEND_FROM, 320);
  if (!apiKey || !from) return false;

  const response = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ from, to, subject, text }),
  });

  if (!response.ok) {
    const detail = await response.text().catch(() => "");
    throw new Error(`Resend API error ${response.status}${detail ? `: ${detail}` : ""}`);
  }

  return true;
}

async function sendBookingNotification({ summary, description, start, end, timeZone }) {
  const to = notificationEmails();
  if (!to.length) return [];

  const subject = `New website booking: ${summary}`;
  const text = [
    "New appointment request received from guoyitangus.com.",
    "",
    `Start: ${start}`,
    `End: ${end}`,
    `Time zone: ${timeZone}`,
    "",
    description,
  ].join("\n");

  if (await sendWithResend({ to, subject, text })) return to;

  const cfg = smtpConfig();
  if (!cfg) return [];

  const transporter = nodemailer.createTransport({
    host: cfg.host,
    port: cfg.port,
    secure: cfg.secure,
    auth: cfg.auth,
  });

  await transporter.sendMail({ from: cfg.from, to, subject, text });

  return to;
}

/** Gregorian weekday 0=Sun … 5=Fri for calendar Y-M-D (UTC noon, unambiguous). */
function calendarWeekdayFri(y, m, d) {
  return new Date(Date.UTC(y, m - 1, d, 12, 0, 0)).getUTCDay() === 5;
}

module.exports = async (req, res) => {
  corsHeaders(req, res);
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const secret = process.env.CALENDAR_INGEST_SECRET;
  if (secret) {
    const hdr = req.headers.authorization || "";
    const token = hdr.startsWith("Bearer ") ? hdr.slice(7) : "";
    if (token !== secret) return res.status(401).json({ error: "Unauthorized" });
  }

  let body;
  try {
    body = await resolveJsonBody(req);
  } catch (err) {
    if (err.message === "BODY_TOO_LARGE")
      return res.status(413).json({ error: "Request body too large" });
    return res.status(400).json({ error: "Invalid JSON" });
  }

  let creds;
  try {
    creds = parseCredentials();
  } catch {
    return res.status(500).json({ error: "Server credential configuration invalid" });
  }
  if (!creds)
    return res.status(503).json({ error: "Calendar booking is not configured" });

  const summaryProvided = trimStr(body.summary, 500);
  const start = trimStr(body.start);
  const end = trimStr(body.end);
  const timeZone = trimStr(body.timeZone) || "America/New_York";
  const contactNameProvided = trimStr(body.contactName, 200);
  const contactPhoneRaw = trimStr(body.contactPhone, 80);
  const contactPhone = contactPhoneRaw || "—";
  const contactEmail = trimStr(body.contactEmail, 200);
  const notes = trimStr(body.notes, 4000);

  if (!start || !end)
    return res.status(400).json({ error: "Missing start or end" });
  const contactName =
    contactNameProvided || "Website form";
  const summary =
    summaryProvided ||
    (contactPhoneRaw ? `Guoyitang · ${contactPhoneRaw}` : "Guoyitang · booking");

  const startD = new Date(start);
  const endD = new Date(end);
  if (Number.isNaN(startD.getTime()) || Number.isNaN(endD.getTime()))
    return res.status(400).json({ error: "Invalid start or end datetime" });
  if (endD <= startD)
    return res.status(400).json({ error: "End must be after start" });

  const dm = /^(\d{4})-(\d{2})-(\d{2})T/.exec(start);
  if (dm) {
    const y = parseInt(dm[1], 10);
    const mo = parseInt(dm[2], 10);
    const da = parseInt(dm[3], 10);
    if (
      y > 0 &&
      mo >= 1 &&
      mo <= 12 &&
      da >= 1 &&
      da <= 31 &&
      calendarWeekdayFri(y, mo, da)
    ) {
      return res.status(400).json({ error: "Clinic is closed on Fridays" });
    }
  }

  const lines = [`联系人：${contactName}`, `电话：${contactPhone}`];
  if (contactEmail) lines.push(`邮箱：${contactEmail}`);
  if (notes) lines.push(`备注：${notes}`);
  lines.push("", "Submitted via guoyitangus.com");

  const description = lines.join("\n");
  const location = trimStr(body.location, 500) || DEFAULT_LOCATION;

  const calendarId = trimStr(process.env.GOOGLE_CALENDAR_ID) || DEFAULT_CALENDAR_ID;

  try {
    const auth = new google.auth.GoogleAuth({
      credentials: creds,
      scopes: ["https://www.googleapis.com/auth/calendar"],
    });
    const authClient = await auth.getClient();
    const cal = google.calendar({ version: "v3", auth: authClient });

    const resource = {
      summary,
      description,
      location,
      start: { dateTime: start, timeZone },
      end: { dateTime: end, timeZone },
    };

    const { data } = await cal.events.insert({
      calendarId,
      requestBody: resource,
      sendUpdates: "none",
    });

    let notifiedEmails = [];
    try {
      notifiedEmails = await sendBookingNotification({
        summary,
        description,
        start,
        end,
        timeZone,
      });
    } catch (err) {
      console.error("calendar-event email notification:", err.message);
    }

    return res.status(201).json({
      ok: true,
      htmlLink: data.htmlLink || null,
      eventId: data.id || null,
      notifiedEmails,
    });
  } catch (err) {
    console.error("calendar-event insert:", err.message);
    const code = calendarErrorCode(err);
    return res.status(502).json({
      error: "Calendar API error",
      detail: code ? String(code) : undefined,
    });
  }
};
