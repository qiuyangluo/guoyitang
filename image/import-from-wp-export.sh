#!/usr/bin/env bash
# Copy homepage assets from a saved WordPress/Elementor export (_files folder).
# Usage (from repo root):
#   bash image/import-from-wp-export.sh
# Or override source:
#   WP_SRC="/path/to/..._files" bash image/import-from-wp-export.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$REPO_ROOT/image"
WP_SRC="${WP_SRC:-/Users/apple/Downloads/主页 - 国医堂 Guoyitang｜法拉盛中医针灸与草药调理专家 纽约中医_30年纽约国医堂_中医妇科男科内科_files}"

if [[ ! -d "$WP_SRC" ]]; then
  echo "WP export folder not found: $WP_SRC" >&2
  exit 1
fi

copy_if() {
  local src_name="$1"
  local dest_name="$2"
  local src="$WP_SRC/$src_name"
  local dest="$DEST/$dest_name"
  if [[ ! -f "$src" ]]; then
    echo "skip (missing in export): $src_name"
    return 0
  fi
  cp -f "$src" "$dest"
  echo "copied: $src_name -> $dest_name"
}

mkdir -p "$DEST"

# Logos & icons
copy_if "cropped-1611981202-logo-125x42.webp" "guoyitang-logo-header-125x42.webp"
copy_if "cropped-1611981202-logo.webp" "guoyitang-logo-footer.webp"

# WeChat promo
copy_if "微信二维码-绿色.jpeg" "guoyitang-wechat-qr.jpg"

# About carousel / clinic
copy_if "IMG_6316-cropped-768x615.jpeg" "photo-clinic-acupuncture-768x615.jpg"
copy_if "国医堂医生团队-e1760394667622-768x614.jpeg" "photo-team-guoyitang-768x614.jpg"
copy_if "IMG_6325-copy-e1762230574894.jpeg" "photo-doctor-jian-peiyu.jpg"
copy_if "4-leguixiang.jpeg" "photo-doctor-yue-herbal.jpg"
copy_if "3-jianpeiyu.jpeg" "photo-doctor-jian-peiyu-alt.jpg"

# Doctor profile cards
copy_if "IMG_6316-cropped-scaled-e1762230660681.jpeg" "photo-doctor-yue-portrait.jpg"

# Therapists (专业服务)
copy_if "fan-profile-985x1024.jpeg" "photo-therapist-fan-kelly.jpg"
copy_if "sun-profile-932x1024.jpeg" "photo-therapist-sun-quanying.jpg"
copy_if "yang-profile.jpeg" "photo-therapist-yang-michael.jpg"
copy_if "IMG_6336-copy-1024x991.jpeg" "photo-therapist-fu-mark.jpg"
copy_if "IMG_6335-copy-1024x963.jpeg" "photo-therapist-liu-yuan-michael.jpg"
copy_if "国医堂刘师傅照片-683x1024.jpeg" "photo-therapist-liu.jpg"

# Services section (stock photos from export)
copy_if "g838e2191cd66f0c2cd707e48166371077903cbbc2a5108f779d22b5138f8ca0e05135f4492cdfe4c954310702e34b4bdebf3ea1454143137deec042bce9d9a42_1280-3666189-1024x682.jpg" "photo-service-herbal-1024x682.jpg"
copy_if "pexels-photo-8139405-8139405-1024x683.jpg" "photo-service-moxibustion-1024x683.jpg"
copy_if "pexels-photo-5473180-5473180-1024x683.jpg" "photo-service-acupuncture-1024x683.jpg"
copy_if "pexels-photo-5927946-5927946-1024x683.jpg" "photo-service-guasha-1024x683.jpg"
copy_if "g02dcea6995756b16ab7d51fdcbd62ec22170f2d8227a94da2e1ededed2e5a4d71dbb4f307ba9bfb38b9a6580fc302db06a6352ba92d5f696ede19c6747f3fc66_1280-6604217-1024x682.jpg" "photo-service-cupping-1024x682.jpg"
copy_if "pexels-photo-275768-275768-1024x685.jpg" "photo-clinic-tuina-massage-768x615.jpg"
copy_if "IMG_6325-copy-e1762230483981-768x617.jpeg" "photo-clinic-tuina-alt-768x617.jpg"

# Recovery story thumbnails (for future use)
copy_if "带状疱疹-1024x576.jpg" "photo-case-shingles-1024x576.jpg"
copy_if "月经不调-1024x576.jpg" "photo-case-menstrual-1024x576.jpg"
copy_if "头重-1024x576.jpg" "photo-case-fatigue-1024x576.jpg"
copy_if "偏头痛-1024x576.jpg" "photo-case-migraine-1024x576.jpg"
copy_if "前列腺炎-1024x576.jpg" "photo-case-prostatitis-1024x576.jpg"
copy_if "腰椎骨错位-1024x576.jpg" "photo-case-lumbar-1024x576.jpg"

# Card-background.png is referenced in Elementor CSS but not saved in _files;
# keep image/card-background.png from live site if already present.
if [[ ! -f "$DEST/card-background.png" ]]; then
  echo "note: Card-background.png not in WP export; download from guoyitangus.com if needed"
fi

echo "Done. Source: $WP_SRC"
