FROM maven:3.8.6-openjdk-11 AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

FROM flink:1.17.1-java11
COPY --from=build /app/target/*.jar /opt/flink/usrlib/app.jar
