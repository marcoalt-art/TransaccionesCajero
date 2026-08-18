#!/bin/bash
echo "Enviando trabajo a Apache Flink..."
docker compose exec jobmanager /opt/flink/bin/flink run /opt/flink/usrlib/TransaccionesCajero-1.0-SNAPSHOT.jar
