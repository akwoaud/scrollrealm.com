# Scrollrealm / Caelterra GitHub Pages Site

This package is a ready-to-upload static website for `scrollrealm.com`.

## What is included

- Complete static HTML/CSS/JS homepage and subpages
- Caelterra-first visual design for a fantasy TCG & TRPG brand
- Product pages, release schedule, static news board, company page, contact page
- SEO metadata, Open Graph image, JSON-LD structured data, `sitemap.xml`, `robots.txt`
- `CNAME` configured for `scrollrealm.com`
- Optimized WebP image assets generated for this project
- No external frontend framework or build step required

## Recommended GitHub Pages deployment

1. Create a repository such as `scrollrealm-site`.
2. Upload all files in this folder to the repository root.
3. In GitHub: Settings → Pages → Deploy from branch → main → root.
4. Confirm the custom domain is `scrollrealm.com`.
5. Configure DNS with your domain provider according to GitHub Pages instructions.
6. Submit `https://scrollrealm.com/sitemap.xml` to Google Search Console and Naver Search Advisor.

## Before launch

- Replace placeholder release windows if needed.
- Replace Formspree placeholder form action with a real form endpoint.
- Replace social links in the footer.
- Add real product purchase links once Shopify, Amazon, Kickstarter, Gamefound, or another sales channel is ready.
- Add real legal text to `privacy.html`.

## Editing content

Static content is in each page's `index.html`.
Reusable sample data is also provided in:

- `data/products.json`
- `data/releases.json`
- `data/news.json`

## Image sources

Images in `assets/images/` are generated original assets for this prototype. The original design concept preview is also included as `assets/images/design-concept-preview.png`.
