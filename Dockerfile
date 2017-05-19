FROM tf-model-server

MAINTAINER Christian Fröhlingsdorf <chris@5cf.de>

RUN mkdir -p /model_export/main_model
ADD ./export /model_export/

CMD ["./tensorflow_model_server", "--port=9000", "--model_name=main_model", "--model_base_path=/model_export/main_model"]