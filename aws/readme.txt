In this project, we are generating a blog post using Foundational models available in the AWS bedrock. The foundational model we used here is "amazon.titan-text-lite-v1".
First step is creting an aws account. 

Services used
1. AWS Lambda
2. AWS API gatewat
3. AWS S3
4. AWS bedrock

We are trying to create a lambda fuction, that will get triggered whenever  we hit out API, and create a blog post as a text file and store it in S3. 
For this we need to create a api request through API gateway.