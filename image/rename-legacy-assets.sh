#!/usr/bin/env bash
# Run from repo root: bash image/rename-legacy-assets.sh
# Renames WordPress-era files to the ASCII names used in HTML/CSS (same format, .jpeg→.jpg where listed).
set -euo pipefail
cd "$(dirname "$0")"

mv_if() {
  if [[ -f "$1" ]]; then
    mv -v "$1" "$2"
  else
    echo "skip (missing): $1"
  fi
}

mv_if "IMG_6316-cropped-768x615.jpeg" "photo-clinic-acupuncture-768x615.jpg"
mv_if "国医堂医生团队-e1760394667622-768x614.jpeg" "photo-team-guoyitang-768x614.jpg"
mv_if "IMG_6325-copy-e1762230574894.jpeg" "photo-doctor-jian-peiyu.jpg"
mv_if "IMG_6316-cropped-scaled-e1762230660681.jpeg" "photo-doctor-yue-portrait.jpg"
mv_if "4-leguixiang.jpeg" "photo-doctor-yue-herbal.jpg"
mv_if "fan-profile-985x1024.jpeg" "photo-therapist-fan-kelly.jpg"
mv_if "sun-profile-932x1024.jpeg" "photo-therapist-sun-quanying.jpg"
mv_if "国医堂刘师傅照片-683x1024.jpeg" "photo-therapist-liu.jpg"
mv_if "微信二维码-绿色.jpeg" "guoyitang-wechat-qr.jpg"
mv_if "cropped-guoyitang-icon-32x32.jpg" "guoyitang-icon-32.jpg"
mv_if "cropped-guoyitang-icon-180x180.jpg" "guoyitang-icon-180.jpg"
mv_if "cropped-1611981202-logo-125x42.webp" "guoyitang-logo-header-125x42.webp"
mv_if "cropped-1611981202-logo.webp" "guoyitang-logo-footer.webp"
echo "Done. If extensions differ (.jpg vs .jpeg), adjust filenames to match your exports."
