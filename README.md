# SimpleMailServer

### Introduction

This project implements a multithreaded HTTP server with basic routing and email-sending functionality. It demonstrates key concepts in networking and higher-layer protocols.


### Features
    
    1. Socket Programming:
           - Uses TCP (IPv4) for client-server communication.
           - Handles multiple client connections concurrently via threading.

    
    2. HTTP Protocol:
          - Processes GET requests for static files.
          - Generates HTTP responses with appropriate status codes (200, 404, 500) and headers.
        
    3. SMTP Protocol:
          - Sends emails using Gmail's SMTP server with STARTTLS encryption for security.      
    
    4. Routing and Query Handling:
         - Supports dynamic routes like /send-email, parsing query parameters for recipient, subject, and message.
              
    5. Content Delivery:
          - Serves static files with MIME type detection.
          - Returns appropriate error pages for invalid routes.


### How It Works

    1. Listens on 127.0.0.1:8081 and processes incoming HTTP requests.
    2. Routes requests to serve files or send emails.
    3. Utilizes threading for handling multiple connections simultaneously.
