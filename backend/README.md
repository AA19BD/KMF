## Quickstart

### 1. Clone project

```bash
git clone https://github.com/AA19BD/KMF.git

```

### 2. Install dependecies

```bash
### 1. CD to root
cd KMF/backend

### 2. Create virtual environment for python
python3 -m venv venv

### 3. Activate virtual environment
source venv/bin/activate

### 4. Install requirements
pip install -r requirements-dev.txt
```

### 3. Run docker for postgres db

```bash
### 1. Run docker container
docker-compose up -d

### 2. Do migrations and initialize with initial_data.py script
bash init.sh

### You can look at the source code of the file, it will just run two commands:
###    - alembic upgrade head (to do migrations)
###    - python -m app.initial_data (to add some start data)
```

### 4. Now you can run app

```bash
### And this is it:
uvicorn app.main:app --reload

```

### 5. Activate pre-commit

[pre-commit](https://pre-commit.com/) is de facto standard now for pre push activities like isort or black.

It will format and notify about minor errors like extra whitespaces when you do git commit to your changes automatically.

```bash
# Install pre-commit
pre-commit install

# Run formatting
pre-commit run --all-files
```

### 6. Running tests

```bash
# Note, it will use second database declared in docker-compose.yml, not default one, to make sure that the main database can be safe, with second database you can do whatever you want :)
pytest

# Output from running above command initially should be:

# collected 7 items

# app/tests/test_auth.py::test_auth_access_token PASSED                                                                       [ 14%]
# app/tests/test_auth.py::test_auth_access_token_fail_no_user PASSED                                                          [ 28%]
# app/tests/test_auth.py::test_auth_refresh_token PASSED                                                                      [ 42%]
# app/tests/test_users.py::test_read_current_user PASSED                                                                      [ 57%]
# app/tests/test_users.py::test_delete_current_user PASSED                                                                    [ 71%]
# app/tests/test_users.py::test_reset_current_user_password PASSED                                                            [ 85%]
# app/tests/test_users.py::test_register_new_user PASSED                                                                      [100%]
#
# ======================================================== 7 passed in 1.75s ========================================================
```

<br>


### 1. Create and apply alembic migration
Every time we modify model.py file, we should do this step. It will automatically create scripts to modify actual postgres database to reflect changes in model.py.

NOTE: scripts will be autogenerated, their should be enough for most cases.

```bash
### Use below commands in root folder in virtualenv ###

# if you see FAILED: Target database is not up to date.
# first use "alembic upgrade head" command

# Create migration with alembic revision
alembic revision --autogenerate -m "create_pet_model"


# File similar to "2022050949_create_pet_model_44b7b689ea5f.py" should appear in `/alembic/versions` folder


# Apply migration using alembic upgrade
alembic upgrade head

# (...)
# INFO  [alembic.runtime.migration] Running upgrade d1252175c146 -> 44b7b689ea5f, create_pet_model
```

PS. Note, alembic is configured in a way that it work with async setup and also detects specific column changes.

## Screenshots

<div>
  <img style="width: 100%" src="screenshots/1.png" />
</div>

<div>
  <img style="width: 100%" src="screenshots/2.png" />
</div>

<div>
  <img style="width: 100%" src="screenshots/3.png" />
</div>

<div>
  <img style="width: 100%" src="screenshots/4.png" />
</div>
