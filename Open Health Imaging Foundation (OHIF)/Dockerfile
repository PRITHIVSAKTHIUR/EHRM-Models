FROM node:18.16.1-slim as json-copier

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
# Clone the application
RUN apt-get update && apt-get install -y git

RUN git clone --recursive https://github.com/OHIF/Viewers.git .

# # COPY ["package.json", "yarn.lock", "preinstall.js", "./"]
# COPY extensions /usr/src/app/extensions
# COPY modes /usr/src/app/modes
# COPY platform /usr/src/app/platform

# Find and remove non-package.json files
#RUN find extensions \! -name "package.json" -mindepth 2 -maxdepth 2 -print | xargs rm -rf
#RUN find modes \! -name "package.json" -mindepth 2 -maxdepth 2 -print | xargs rm -rf
#RUN find platform \! -name "package.json" -mindepth 2 -maxdepth 2 -print | xargs rm -rf

# Copy Files
FROM node:18.16.1-slim as builder
RUN apt-get update && apt-get install -y build-essential python3
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY --from=json-copier /usr/src/app .

# Run the install before copying the rest of the files
RUN yarn config set workspaces-experimental true
RUN yarn install --frozen-lockfile --verbose

COPY . .

# To restore workspaces symlinks
RUN yarn install --frozen-lockfile --verbose

ENV PATH /usr/src/app/node_modules/.bin:$PATH
ENV QUICK_BUILD true
# ENV GENERATE_SOURCEMAP=false
# ENV REACT_APP_CONFIG=config/default.js

RUN yarn run build
# Stage 3: Bundle the built application into a Docker container
# which runs Nginx using Alpine Linux
FROM nginxinc/nginx-unprivileged:1.25-alpine as final
#RUN apk add --no-cache bash
USER nginx
COPY --chown=nginx:nginx nginx.conf /etc/nginx/conf.d/default.conf
COPY --chown=nginx:nginx app-config.js /usr/share/nginx/html/app-config.js
COPY --from=builder /usr/src/app/platform/app/dist /usr/share/nginx/html
# In entrypoint.sh, app-config.js might be overwritten, so chmod it to be writeable.
# The nginx user cannot chmod it, so change to root.
USER root
RUN chmod 666 /usr/share/nginx/html/app-config.js
USER nginx
CMD ["nginx", "-g", "daemon off;"]
