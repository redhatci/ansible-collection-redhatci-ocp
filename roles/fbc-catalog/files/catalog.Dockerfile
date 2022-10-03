FROM quay.io/operator-framework/opm:latest
ENTRYPOINT ["/bin/opm"]
CMD ["serve", "/configs"]
ADD catalog /configs
LABEL operators.operatorframework.io.index.configs.v1=/configs
LABEL maintainer="Telco DCI team" quay.expires-after=5h