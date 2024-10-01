Mọi người nhớ sử dụng môi trường ảo nhé py -m venv .venv

sau đó chạy lệnh: .venv/scripts/activate

sau đó cài: pip install -r requirements.txt

tạo secret_key: python -c "import secrets; print(secrets.token_urlsafe(32))"
