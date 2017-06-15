FROM tf-model-server

MAINTAINER Christian Fröhlingsdorf <chris@5cf.de>

RUN mkdir /model_export
ADD ./export /model_export/

CMD ["./tensorflow_model_server", "--port=9000", "--model_name=gender_model", "--model_base_path=/model_export/gender_model"]