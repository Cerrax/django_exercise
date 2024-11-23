#---------- STAGE FOR ALL BUILDS ----------
FROM node:22.11 AS common-base

RUN mkdir /app
WORKDIR /app

RUN npm install -g @vue/cli

EXPOSE 5173
EXPOSE 8000

COPY . /app/
RUN npm install


#---------- STAGE FOR DEPLOYMENT ----------
FROM common-base AS deploy-build

RUN npm run build

FROM scratch AS deploy

COPY --from=deploy-build /app/dist .


#---------- STAGE FOR DEVELOPMENT ----------
FROM common-base AS development

ENTRYPOINT ["./default.entrypoint.sh"]
