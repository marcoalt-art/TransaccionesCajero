package com.ejemplo.streaming;

import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;

import java.util.Properties;

public class WordCountKafka {

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        Properties properties = new Properties();
        properties.setProperty("bootstrap.servers", "kafka:9092");
        properties.setProperty("group.id", "cajero-group");

        FlinkKafkaConsumer<String> consumer = new FlinkKafkaConsumer<>(
                "cajero-events",
                new SimpleStringSchema(),
                properties
        );

        DataStream<String> stream = env.addSource(consumer);

        DataStream<String> processedStream = stream.map(new MapFunction<String, String>() {
            @Override
            public String map(String value) throws Exception {
                // Procesamiento de la transacción del cajero y validación de reglas de alerta
                if (value.contains("\"monto\":") && value.contains("\"monto_entregado\":")) {
                    return value.replace("}", ",\"alerta\":\"PROCESADO_OK\"}");
                }
                return value;
            }
        });

        FlinkKafkaProducer<String> producer = new FlinkKafkaProducer<>(
                "cajero-results",
                new SimpleStringSchema(),
                properties
        );

        processedStream.addSink(producer);

        env.execute("TransaccionesCajeroJob");
    }
}
