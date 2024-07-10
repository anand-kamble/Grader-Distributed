# Use the official NGINX image from the Docker Hub
FROM nginx:latest

# Remove the default NGINX configuration file
RUN rm /etc/nginx/nginx.conf

# Copy your custom NGINX configuration file to the appropriate location
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 to allow external traffic
EXPOSE 80

# Start the NGINX server
CMD ["nginx", "-g", "daemon off;"]
