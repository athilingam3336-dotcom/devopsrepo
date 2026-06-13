FROM nginx:1.25-alpine

# Copy app
COPY index.html /usr/share/nginx/html/index.html

# Inject API base URL at container start via envsubst
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
