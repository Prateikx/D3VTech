Project Name
This project aims to parse product JSON and store it in a MariaDB table for future management using CRUD operations. The ability to create, modify, and delete products is limited to super users with administrative privileges. The project is implemented using the FAST API framework.

Features
User Authentication: The API supports user authentication using JWT (JSON Web Token). Users can obtain an access token by providing valid credentials and use it to access protected endpoints.
User Registration: New users can sign up by providing their name, email, and password. The API securely stores hashed passwords in the database.
Product Retrieval: Users can retrieve information about a specific product by providing its SKU (stock keeping unit).
Product Creation: Authorized users, specifically the "admin" role, can create new products by providing details such as name, category, SKU, price, and quantity.
Product Update: Authorized users can update the name of a product by specifying its SKU.
Product Deletion: Authorized users can delete a product from the inventory by specifying its SKU.
Category Listing: Users can retrieve a list of distinct categories available in the inventory.


Electronics Store Catalog API
This project provides a RESTful API for managing the inventory of a local electronics store. The current manual inventory tracking system at the store is being replaced with a modern cataloging system, enabling seamless integration with mobile and desktop applications in the future.

Features
User Authentication: The API supports user authentication using JWT (JSON Web Token). Users can obtain an access token by providing valid credentials and use it to access protected endpoints.
User Registration: New users can sign up by providing their name, email, and password. The API securely stores hashed passwords in the database.
Product Retrieval: Users can retrieve information about a specific product by providing its SKU (stock keeping unit).
Product Creation: Authorized users, specifically the "admin" role, can create new products by providing details such as name, category, SKU, price, and quantity.
Product Update: Authorized users can update the name of a product by specifying its SKU.
Product Deletion: Authorized users can delete a product from the inventory by specifying its SKU.
Category Listing: Users can retrieve a list of distinct categories available in the inventory.


Technologies Used
The following technologies and libraries are used in this project:

FastAPI: A modern, fast (high-performance), web framework for building APIs with Python.
Passlib: A password hashing library providing safe and secure password hashing algorithms.
MariaDB: An open-source relational database management system for storing and retrieving data.
Pydantic: A data validation and parsing library used for defining the API's request and response models.
python-dotenv: A library for loading environment variables from a .env file.
JWT (JSON Web Token): A standard for securing and exchanging claims between two parties. JWT is used for user authentication in this API.


API Documentation
The API endpoints, their functionalities, and request/response models are documented using Swagger UI. You can access the API documentation by navigating to http://localhost:<port>/docs in your browser after starting the application.

Conclusion
With this Electronics Store Catalog API, we aim to simplify and streamline the inventory management process for the local electronics store. By leveraging the power of a RESTful API and incorporating user authentication, the store can efficiently manage its products and prepare for future integrations with mobile and desktop applications.

We hope that this project serves as a solid foundation for enhancing the store's inventory management capabilities and contributes to its growth and success.