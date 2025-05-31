# Event Bridge 

![](./diagram.png)
- API Gateway serves as the public-facing HTTP endpoint, receiving external client requests.

- It invokes a Lambda function (worker1) that processes incoming data and forwards it to an Amazon EventBridge bus.
- EventBridge acts as the central event routing mechanism.
- Events are then routed to two separate processing flows:
  - A Translate pipeline using a Lambda function (proc1)
  - A Sentiment Analysis pipeline, also using a Lambda function (proc1)