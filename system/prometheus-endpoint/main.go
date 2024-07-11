package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

type Metrics struct {
	CPU          string  `json:"cpu"`
	ResponseTime float64 `json:"responseTime"`
}

func main() {
	router := gin.Default()

	router.GET("/", func(ctx *gin.Context) {
		res, err := http.Get("http://localhost:5000/metrics")
		if err != nil {
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

		ctx.String(http.StatusOK, "%s", fmt.Sprintf("rs_cpu %s", metric.CPU))
	})

	router.Run()
}
