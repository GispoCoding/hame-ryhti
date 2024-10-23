FROM public.ecr.aws/lambda/python:3.12

# Install Python dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copy function code
COPY lambdas/db_manager/db_manager.py ${LAMBDA_TASK_ROOT}

COPY alembic.ini ${LAMBDA_TASK_ROOT}
COPY database/migrations ${LAMBDA_TASK_ROOT}/database/migrations/

COPY \
    database/db_helper.py \
    database/base.py \
    database/codes.py \
    database/models.py \
    database/triggers.py \
    ${LAMBDA_TASK_ROOT}/database/

CMD [ "db_manager.handler" ]
