# chamuyo-bot
solo humo

pip install openai

pip install requests




cd venv/lib/python3.10/site-packages/
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip lambda_function.py


cron(0 13 ? * MON-FRI *)
