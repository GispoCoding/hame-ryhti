FROM public.ecr.aws/lambda/python:3.12

# Install Python dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY database/mml_loader/mml_loader.py ${LAMBDA_TASK_ROOT}/mml_loader.py
COPY database/db_helper.py  ${LAMBDA_TASK_ROOT}/db_helper.py
COPY database/base.py ${LAMBDA_TASK_ROOT}/base.py
COPY database/codes.py ${LAMBDA_TASK_ROOT}/codes.py
COPY database/models.py ${LAMBDA_TASK_ROOT}/models.py


CMD [ "mml_loader.handler" ]
