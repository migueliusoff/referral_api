FROM referral_api as app

FROM nginx:1.27-alpine

RUN rm -rf /etc/nginx/conf.d
COPY deploy/nginx/host.conf /etc/nginx/conf.d/default.conf
COPY --from=app /app/static /app/static