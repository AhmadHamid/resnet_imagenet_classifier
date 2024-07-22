package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
    "os"
	"github.com/gin-gonic/gin"
)

type Metrics struct {
	CPU           string  `json:"cpu"`
	InferenceTime float64 `json:"inferenceTime"`
	ResponseTime  float64 `json:"responseTime"`
	Accuracy      float64 `json:"accuracy"`
}

func main() {
    metricUrl := os.Getenv("METRIC_URL")
	router := gin.Default()

	router.GET("/metrics", func(ctx *gin.Context) {
		// TODO: Set Timeout for GET request
		res, err := http.Get(metricUrl)
		if err != nil {
			ctx.String(http.StatusInternalServerError, "%s", "Internal Error")
			log.Panic(err)
		}

		body, err := io.ReadAll(res.Body)
		if err != nil {
			log.Panic(err)
		}

		var metric Metrics

		if err := json.Unmarshal(body, &metric); err != nil {
			log.Panic(err)
		}

		ctx.String(http.StatusOK, "%s", fmt.Sprintf("rs_cpu %s\nrs_inference_time %f\nrs_response_time %f\nrs_accuracy %f", metric.CPU, metric.InferenceTime, metric.ResponseTime, metric.Accuracy))
	})

	router.Run(":8081")
}
