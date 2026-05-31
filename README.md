<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/31b6820c-83a7-423c-92ba-81388c49b4a7

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`
# artemadera-django

## Деплой (статика и админка)

При `DEBUG=False` Django **не** отдаёт CSS/JS админки сам. В проекте включён **WhiteNoise** и задан `STATIC_ROOT`. На каждом деплое после установки зависимостей выполните:

```bash
python manage.py collectstatic --noinput
```

Иначе страница `/admin/` будет без стилей (Unfold и стандартная админка лежат в пакетах и попадают в ответ только через собранные файлы в `staticfiles/`).
