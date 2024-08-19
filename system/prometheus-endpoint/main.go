package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

type Metrics struct {
	InferenceTime float64 `json:"inferenceTime,omitempty"`
	ResponseTime  float64 `json:"responseTime,omitempty"`
	Requests      int     `json:"requests,omitempty"`
	Accuracy      float64 `json:"accuracy,omitempty"`
}

var inferenceTime = promauto.NewGauge(prometheus.GaugeOpts{
	Name: "rn_inference_time_total_seconds",
	Help: "Total inference time for all requests in seconds",
})

var responseTime = promauto.NewGauge(prometheus.GaugeOpts{
	Name: "rn_response_time_total_seconds",
	Help: "Total response time for all requests in seconds",
})

var accuracy = promauto.NewGauge(prometheus.GaugeOpts{
	Name: "rn_accuracy",
	Help: "123",
})

var requests = promauto.NewCounter(prometheus.CounterOpts{
	Name: "rn_requests_responded_total",
	Help: "Total responded requests",
})

func recordMetrics() {
	go func() {
		for {
			var metric Metrics
			// TODO: Set Timeout for GET request
			res, err := http.Get("http://localhost:5000/metrics")
			if err != nil {
				metric = Metrics{}
				log.Panic(err)
			} else {
				body, err := io.ReadAll(res.Body)
				if err != nil {
					metric = Metrics{}
					log.Panic(err)
				} else {
					if err := json.Unmarshal(body, &metric); err != nil {
						metric = Metrics{}
						log.Panic(err)
					}
				}
			}

			inferenceTime.Set(metric.InferenceTime)
			responseTime.Set(metric.ResponseTime)
			accuracy.Set(metric.Accuracy)
			requests.Add(float64(metric.Requests))
			time.Sleep(2 * time.Second)
		}
	}()
}

func main() {
	recordMetrics()

	http.Handle("/metrics", promhttp.Handler())
	http.ListenAndServe(":2112", nil)
}
