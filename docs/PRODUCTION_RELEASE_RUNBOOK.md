# ArteMadera: production release runbook

Цель релиза: развернуть проверенный коммит `9bd5b50` на `artemadera.ru` без замены рабочей `db.sqlite3`, `.venv` и пользовательского `media/`.

Предыдущий production SHA: `34ca576`.

## Единственный ручной шаг владельца

Восстановить вход существующим ключом на production-ВМ и проверить его одной командой:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub ubuntu@46.21.244.6
ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes ubuntu@46.21.244.6 'id -un'
```

Ожидаемый ответ второй команды: `ubuntu`. Первый шаг нужен только потому, что публичный ключ с отпечатком `SHA256:l/B/eq0xf/tV7iEr9MA871GrjSbUB+Dj8K6qC4D5X+s` указан в метаданных ВМ, но сейчас не принимается её `sshd`. Не передавать пароль или приватный ключ в чат.

После появления рабочего SSH-доступа остальной выпуск выполняется по шагам ниже.

## 1. Найти фактический сервис и каталог

```bash
ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes ubuntu@46.21.244.6
sudo -v
sudo systemctl list-unit-files --type=service | grep -Ei 'arte|gunicorn'
sudo find /var/www -maxdepth 4 -type d -name .git -print
```

Проверить найденный unit командой `sudo systemctl cat ИМЯ.service`. Из `WorkingDirectory` взять `APP_DIR`, из `ExecStart` — фактический Python/venv. Не угадывать имя сервиса или путь.

Далее в примерах:

```bash
APP_DIR=/var/www/ФАКТИЧЕСКИЙ_КАТАЛОГ
SERVICE=ФАКТИЧЕСКИЙ_UNIT.service
PYTHON="$APP_DIR/ФАКТИЧЕСКИЙ_VENV/bin/python"
TARGET_SHA=9bd5b50
PREVIOUS_SHA=34ca576
cd "$APP_DIR"
```

## 2. Preflight и резервная копия

```bash
git status --short --branch
git fetch origin main
test "$(git rev-parse origin/main)" = "$TARGET_SHA"
git diff --exit-code "$PREVIOUS_SHA" "$TARGET_SHA" -- db.sqlite3 .venv media
test -f db.sqlite3
sqlite3 db.sqlite3 'PRAGMA integrity_check;'
```

Ожидается `ok`; `git diff` для БД, окружения и media должен быть пустым.

```bash
BACKUP_DIR="/var/backups/artemadera/$(date +%Y%m%d-%H%M%S)-$PREVIOUS_SHA"
sudo install -d -m 700 "$BACKUP_DIR"
sudo cp --preserve=all db.sqlite3 "$BACKUP_DIR/db.sqlite3"
sudo cp --preserve=all "$(sudo systemctl show -p FragmentPath --value "$SERVICE")" "$BACKUP_DIR/"
git rev-parse HEAD | sudo tee "$BACKUP_DIR/source-sha.txt"
sudo sqlite3 "$BACKUP_DIR/db.sqlite3" 'PRAGMA integrity_check;'
```

Не продолжать, если SHA, integrity check или backup не подтверждены.

## 3. Проверка плана и выпуск

```bash
git merge-base --is-ancestor "$PREVIOUS_SHA" "$TARGET_SHA"
git diff --check "$PREVIOUS_SHA" "$TARGET_SHA"
git diff --name-status "$PREVIOUS_SHA" "$TARGET_SHA"
git switch main
git merge --ff-only "$TARGET_SHA"
git diff --quiet "$PREVIOUS_SHA" "$TARGET_SHA" -- requirements.txt || "$PYTHON" -m pip install -r requirements.txt
"$PYTHON" manage.py check
"$PYTHON" manage.py makemigrations --check --dry-run
"$PYTHON" manage.py migrate --plan
```

План должен содержать только `main.0086`–`main.0090`. Затем:

```bash
"$PYTHON" manage.py migrate --noinput
"$PYTHON" manage.py collectstatic --noinput
sudo systemctl restart "$SERVICE"
sudo systemctl is-active "$SERVICE"
sudo systemctl status "$SERVICE" --no-pager -l
sudo journalctl -u "$SERVICE" --since '-5 minutes' --no-pager
```

Ожидается `active`, без traceback и циклических рестартов.

## 4. HTTP/SEO smoke

```bash
curl -fsSI http://artemadera.ru/
curl -fsSI https://www.artemadera.ru/pokraska/
curl -fsSI 'https://artemadera.ru/otdelka/?utm_source=qa'
curl -fsS https://artemadera.ru/robots.txt
curl -fsS https://artemadera.ru/sitemap.xml | xmllint --noout -
curl -fsS https://artemadera.ru/pokraska | grep -F '"@type": "WebSite"'
curl -fsS https://artemadera.ru/pokraska | grep -F '<link rel="canonical" href="https://artemadera.ru/pokraska"'
```

Ожидаемые редиректы — одним переходом на HTTPS apex; `/otdelka/` должен сразу вести на `https://artemadera.ru/otdelochnye-raboty` с сохранением query string. Sitemap не должен содержать удалённые URL `bani-i-sauny` и `konsyerzhnaya`.

## 5. Production QA заявки

Через обычный браузер отправить одну явно маркированную заявку:

- имя: `QA release 9bd5b50`;
- телефон: заранее согласованный тестовый номер владельца;
- сообщение: `Тест после релиза, не обрабатывать как клиента`;
- URL с `?utm_source=qa&utm_campaign=seo-release&yclid=qa-9bd5b50`.

Подтвердить отдельно:

1. UI показал успешную отправку без повторной заявки.
2. В `ContactLead` сохранены UTM/yclid, landing page и page URL.
3. Создана связанная CRM-сделка с теми же атрибутами.
4. Email действительно получен хотя бы одним адресатом; одной SMTP-конфигурации недостаточно.
5. В браузере вызваны цели `LEAD_SEND` и профильная `LEAD_*`; в консоли нет JS-ошибок.

После фиксации результатов пометить тестовую CRM-сделку как тест/спам или удалить её согласованным способом, не затрагивая реальные заявки.

## 6. artemadera.su

Сейчас `artemadera.su` и `www.artemadera.su` указывают на `46.21.246.24`, отдают отдельную страницу по HTTP и не принимают HTTPS. Код на ВМ `.ru` не изменит это поведение.

Не менять DNS, пока не подтверждены владелец ресурса `46.21.246.24`, доступ к его nginx и сертификат для `.su`. После получения контроля настроить на старом endpoint один постоянный редирект для любого пути и query string:

```nginx
return 301 https://artemadera.ru$request_uri;
```

До переключения проверить конфигурацию `nginx -t`, после — четыре варианта: HTTP/HTTPS и apex/www. Не удалять DNS-записи до устойчивого 301 и переобхода.

## 7. Rollback

Если приложение не стартует или критический путь не проходит:

```bash
cd "$APP_DIR"
sudo systemctl stop "$SERVICE"
"$PYTHON" manage.py migrate main 0085 --noinput
git switch --detach "$PREVIOUS_SHA"
"$PYTHON" manage.py collectstatic --noinput
sudo systemctl start "$SERVICE"
sudo systemctl is-active "$SERVICE"
```

Если обратные миграции не завершились, восстановить БД из созданной копии только при остановленном сервисе:

```bash
sudo systemctl stop "$SERVICE"
sudo cp --preserve=all "$BACKUP_DIR/db.sqlite3" "$APP_DIR/db.sqlite3"
git switch --detach "$PREVIOUS_SHA"
"$PYTHON" manage.py collectstatic --noinput
sudo systemctl start "$SERVICE"
```

После rollback повторить HTTP smoke и тест сохранения заявки. Не объявлять rollback успешным только по статусу systemd.
