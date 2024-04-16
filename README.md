Vivid Arts Studio
As a leading photography studio, we specialize in capturing moments that transcend the ordinary, providing our clients with timeless and evocative images.

Overview
At VividArt Studios, we find ourselves at an exciting crossroads in our journey through the vibrant world of photography. As we strive to deliver personalized transformations that transcend the ordinary, we've identified some challenges in our current photo editing tools, particularly during the crucial phase of photo uploads. The need for seamless, dynamic transformations has become increasingly apparent, prompting us to seek innovative solutions that align with the growth of our studio.
In the evolving landscape of technology, we recognize the importance of not only meeting but exceeding the expectations of our clients. The complexity of photo uploads demands a robust system that not only enhances the editing experience but also ensures a smooth and efficient workflow. As VividArt Studios expands, the scalability of our current infrastructure has become a focal point, with occasional performance hiccups hindering our ability to provide consistent, high-quality services. To address these challenges, we are reaching out to you, the talented minds in the realm of cloud engineering, to collaborate on the development of a solution that not only meets our current needs but also positions us for future growth. We're seeking a transformative approach that seamlessly integrates into our workflow, facilitating dynamic and personalized edits while ensuring scalability and performance. Let's embark on this exciting journey together, leveraging modern technologies to create a system that not only meets the demands of today but anticipates the needs of tomorrow. Your contribution to this project will not only elevate our studio but also shape the future of VividArt's artistic endeavors. Get ready to dive into the world of innovation and collaboration, where your skills will be the brushstrokes that paint the canvas of our success.

**Let's Break it down**
Key Factors to think about
**Containerization:** Implement a solution that allows the seamless deployment of applications across different environments using containerization. This ensures flexibility and consistency, enabling the system to adapt to varying infrastructures.
**Automated Photo Editing Workflow:**Design an automated workflow for photo editing that enhances the efficiency of the editing tools. This could involve the use of background processes or serverless functions triggered by photo uploads, minimizing manual intervention.
**Cloud Storage for Accessibility:**Utilize cloud storage solutions, to store and manage photos. This not only ensures easy accessibility but also provides a scalable and durable storage infrastructure.
**User-Friendly Interfaces:**Focus on creating intuitive and user-friendly interfaces for both photographers and clients. This includes streamlining the photo upload process and providing feedback options.
**Infrastructure as Code (IaC):**Implement Infrastructure as Code to automate the provisioning and management of infrastructure resources. 
**Monitoring and Analytics:** Identify bottlenecks, and gather insights for continuous improvement.
**Continuous Integration/Continuous Deployment (CI/CD):**Implement CI/CD pipelines to automate the testing and deployment of changes, ensuring a rapid and reliable release cycle.

**The Solution**
1. Containerization
	docker image for the flask application
	docker image for lambda function runtime
2. Automated Photo Editing Workflow: lamda function to process the photos
3. Cloud Storage for Accessibility: 
	source-photo bucket for uploading photos
	modified-photo bucket for storing processed photos
4. User-Friendly Interfaces:
5. Infrastructure as Code (IaC): Terraform
6. Monitoring and Analytics: Amazon CloudWatch to track system performance, identify bottlenecks
7. Continuous Integration/Continuous Deployment (CI/CD): AWS CodePipeline and AWS CodeBuild 

**Terraform script**
This Terraform script sets up the infrastructure required for your photo processing application on AWS. It creates S3 buckets for source and processed photos, an SNS topic for notifying about photo processing completion, a CloudWatch Logs group for Lambda function logging, an IAM role for the Lambda function, and attaches necessary permissions policies to it. Additionally, it creates a Lambda function and attaches an event source mapping to trigger it when new photos are uploaded to the source S3 bucket.
**Here's a breakdown of the script:**
1. Provider Configuration: Specifies the AWS provider and region.
2. S3 Bucket Creation: Creates two S3 buckets, one for storing source photos and the other for storing processed photos.
3. SNS Topic Creation: Creates an SNS topic for notifying about photo processing completion.
4. CloudWatch Logs Group: Creates a CloudWatch Logs group for the Lambda function's logging.
5. IAM Role for Lambda: Defines an IAM role for the Lambda function with an assume role policy allowing Lambda service to assume the role.
6. IAM Policies: Defines IAM policies for granting permissions to the Lambda function to access S3 buckets and publish messages to the SNS topic.
7. Lambda Function Creation: Creates the Lambda function with the specified runtime, handler, and environment variables. It also attaches the CloudWatch Logs group and defines dependencies on the IAM role.
8. Event Source Mapping: Creates an event source mapping between the S3 bucket and the Lambda function to trigger the function when new photos are uploaded.
9. The aws_ecr_repository resource creates a private repository named "lambda_image" in Amazon ECR.
10. The aws_ecr_repository_policy resource attaches permissions for the Lambda function to pull the Docker image from the ECR repository.
11. The aws_lambda_function resource's image_uri attribute is set to the repository URL of the Docker image in the ECR repository.
This configuration ensures that the Lambda function uses the Docker image from the specified ECR repository.

**Lambda function**
The provided Python script is a Lambda function intended to be used for image processing. It responds to S3 object creation events, enhances the uploaded images, saves the processed images to a different S3 bucket, generates pre-signed URLs for the processed images, and publishes a message to an SNS topic with the pre-signed URL.
**Here's a summary of what the script does:**
1. Enhancement and Processing: It enhances the uploaded image using adjustable color adjustments and optional filters.
2. S3 Operations: It downloads the uploaded image from the source S3 bucket, processes it, and then uploads the processed image to a different destination bucket.
3. Pre-signed URL Generation: It generates a pre-signed URL for accessing the processed image, ensuring secure access to the image for a limited time.
4. SNS Message Publication: It publishes a message to an SNS topic with information about the processing completion, including the pre-signed URL for the processed image.
5. Error Handling: It includes error handling to catch exceptions and provide informative error messages.

**Flask Application Integration:**
1. Subscribe your Flask application to the SNS topic so that it receives notifications when processing is complete. 
2. When processing is complete: the Lambda function publishes a message to the SNS topic with details about the processed image.
3. The Flask application receives this notification and update the UI accordingly: Flask Application Allows Download of Processed Image: 4. The Flask application provides a button to download the processed image using the pre-signed URL generated by the Lambda function. This button is displayed when the processed image URL is available.

**UI Updates:**
Displays a success message on the Flask application upon successful upload of the image.
When processing is complete, displays a message indicating the completion and provide a link/button for users to download the processed image using the pre-signed URL


