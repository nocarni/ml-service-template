# ml-service-template
This repository contains a *somewhat* completed RESTful API project that is used to highlight software architecture patterns I always reuse. I did not invent these patterns, in fact, I learned them from the book by Harry Percival and Bob Gregory, [Architecture Patterns with Python (also known as cosmic python)](https://www.cosmicpython.com/).

The purpose of this project is to illustrate the design and benefits of the "Three-Layered Architecture" (TLA) and how it creates maintainable and scalable software projects. The simplest and most intuitive reason I can give as to why the TLA is so effective is that each layer corresponds to a level of testing, unit tests, integration tests, and e2e tests (the full testing pyramid). If code is written with high test coverage and follows the practices of maximizing unit tests and minimizing e2e tests (although you still want some) then you can confidently make changes to the codebase, improving the developer experience dramatically.

You guessed right, the TLA has 3 layers which each have distinct responsibilities. We will talk about these layers going from top to bottom (the initial request going down to the database) and how to test each one of them.

- Web Framework Layer
- Service Layer
- Adapters and Domain Models Layer

The Web Framework Layer receives the requests, instantiates any dependencies the service layer needs, then calls the service layer using the requests and dependencies. Inside, the service layer defines abstract interfaces that describe interactions with external systems and works with domain models to perform the business rules and operations. The domain models that are operated on within the service layer are retrieved via adapters, bridging data located in external services and converting them into domain models. 

### Web Framework Layer
Ok great, but what does this actually look like for this laye? Using the code from this repository, in [app.py](src/example/entrypoints/app.py), the web framework layer using FastAPI, we call the service function while also instantiating a *real* `UnitOfWork` instance. These instances contain the configuration and function calls to connect to the external dependencies (databases, 3rd party APIs) and we inject them into the function since it needs them to complete the operation, hence dependency inversion.

```
job_postings = services.predict_job_postings(
    user,
    unit_of_work.MachineLearningUnitOfWork(),
    unit_of_work.FeatureStoreUnitOfWork()
)
```

Since this is the level at which end-to-end tests are executed, we must use the actual dependencies, and those are setup with docker-compose prior to running this test script. The test cases should only include the logic written at the web framework level and not include tests for specific domain models as that should be covered in unit tests.


### Service Layer
The way I like to think about the service layer is that it depends totally on abstractions, and ideally it should read like pseudo-code. This is where the core of the business logic resides. It accesses any data it needs through abstractions like the `Repository` and uses the `UnitOfWork` to group together atomic operations that match the business rules.


Now for testing the service layer, You might of noticed that I emphasized *real* instances in the Web Framework Layer, a cool trick we can do is to create *Fake* instances that adhere to the same abstract interfaces and pass those in during unit tests! Take the FakeFeatureStoreRepository as an example. This adheres to the same interface as the real FeatureStoreRepository but it simply returns test fixtures that you instantiate this object with! Since the service layer depends entirely on abstractions, we can pass in Fake dependencies and test the business logic regardless of where the data is coming from!
```
class FakeFeatureStoreRepository(repo.AbstractFeatureStoreRepository):
    def __init__(self, resume_keywords):
        self.resume_keywords = resume_keywords

    def get_resume_keywords(self, user=None):
        return self.resume_keywords
```


### Adapters and Domain Models Layer
The way I think about Adapters and Domain Models is that the adapters (which could include an ORM, in our case it's the repository pattern) connect to external depedencies (database, file system), retrieve data, and parse that data into a Domain Model. The Domain Model encapsulates an entity within the current domain and contains any functions needed. The Domain Model is handed to the service layer for further operations. These patterns each focus on a single responsibility.

For testing this layer, domain models are actually quite easy. Create a test fixture and initialize the domain object similar to how the adapter does it, and use this fixture to test any functions created for that class. An example in this project is testing `User.to_dataframe()` as seen [here](./tests/unit/test_domain_models.py), nothing to complicated.

Testing the external dependency involves another example of leveraging the dependency-inversion principle. Instead of assuming the connection to a specific database inside the adapter, we pass in the connection string during initialization. This allows use to point the adapter to different databases. In production, we would point it to a postgres database, during local development a local postgres, and during testing a sqlite in memory database. This pattern decouples the actual service logic from the underlying infrastructure implementation.

Currently, this is not implemented in the project, but here is an example. The code below would be executed and the `config.get_database_config()` returns a different sqlalchemy connection string based on which environment it's being executed in.
```
DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_database_config(os.environ["ENVIRONMENT"])
    )
)
class DatabaseUnitOfWork(AbstractDatabaseUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory
```
