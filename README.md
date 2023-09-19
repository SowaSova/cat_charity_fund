# Кошачий благотворительный фонд
### Сервис для поддержки котиков!

####
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

Для запуска проекта:

```
git clone git@github.com:SowaSova/cat_charity_fund.git
cd cat_charity_fund
```
win:
```
python -m venv venv
. venv/Scripts/activate
```
*nix:
```
python3 -m venv venv
. venv/bin/activate
```

```
pip install -r requirements.txt
```
```
uvicorn app.main:app --reload
```
>[Документация](http://localhost:8000/docs)
