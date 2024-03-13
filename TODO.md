## Moving forward
- Implement trading package    
  - [ ] Implement working orders service
    - [ ] Implement V2 GET /workingorders
      - [ ] Implement v2 GET /workingorders response model
      - [ ] Implement v2 GET /workingorders method
    - [ ] Implement V2 POST /workingorders
      - [ ] Implement v2 POST /workingorders/otc request model
      - [ ] Implement v2 POST /workingorders/otc method
    - [ ] Implement V2 DELETE /workingorders
      - [ ] Implement V2 DELETE /workingorders/otc/{dealId} method
    - [ ] Implement V2 PUT /workingorders/otc/{dealId}
      - [ ] Implement V2 DELETE /workingorders/otc/{dealId} request model
      - [ ] Implement V2 DELETE /workingorders/otc/{dealId} method

- Implement markets package
  - [ ] Implement markets service
    - [ ] Implement market navigation get method
    - [ ] Implement market navigation get method tests
    - [ ] Implement market navigation get node method and model
    - [ ] Implement market navigation get node method tests
    - [ ] Implement get markets method
    - [ ] Implement get markets method tests
    - [ ] Implement get market with search term method
    - [ ] Implement get market with search term method tests
    - [ ] Implement get market by epic method
    - [ ] Implement get market by epic method tests
  - [ ] Implement prices service
    - [ ] Implement get historical prices by epic, resolution and number of points method
    - [ ] Implement get historical prices by epic, resolution and number of points method tests
    - [ ] Implement get historical prices by epic, resolution, start and end date method
    - [ ] Implement get historical prices by epic, resolution, start and end date method tests

- Implement costs and charges package
  - [ ] Implement costs and charges service
    - [ ] Implement POST v1 /indicativecostsandcharges/open
      - [ ] Implement POST v1 /indicativecostsandcharges/open request model
      - [ ] Implement POST v1 /indicativecostsandcharges/open response model
      - [ ] Implement POST v1 /indicativecostsandcharges/open method
    - [ ] Implement POST v1 /indicativecostsandcharges/close
      - [ ] Implement POST v1 /indicativecostsandcharges/close request model
      - [ ] Implement POST v1 /indicativecostsandcharges/close response model
      - [ ] Implement POST v1 /indicativecostsandcharges/close method
    - [ ] Implement POST v1 /indicativecostsandcharges/edit
      - [ ] Implement POST v1 /indicativecostsandcharges/edit request model
      - [ ] Implement POST v1 /indicativecostsandcharges/edit response model
      - [ ] Implement POST v1 /indicativecostsandcharges/edit method


## Refinement

- [x] Module renaming:
        Where module name is the same as package name rename that module to service.
            1. authentication.authentication -> authentication.service
            2. trading.positions.positions -> trading.positions.service
            3. trading.working_orders.working_orders -> trading.working_orders.service
- [ ] Create either a @decorator or a function for general request processing e.g:
  ```
    def handle_request(request_func: callable, endpoint: str, headers_update: dict = None):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                url = f"{self.base_url}/{endpoint.format(*args, **kwargs)}"
                headers = self.headers.update(headers_update) if headers_update else self.headers
                request_name = func.__name__.split('_').join(' ').capitalize()

                try:
                    response = request_func(url, headers=headers, *args, **kwargs)
                    if response.status_code == 200:
                        return func(self, response.json())
                    else:
                        logger.error(
                            "%s request failed with status code %s: %s",
                            request_name,
                            response.status_code,
                            response.text,
                        )
                        raise PositionsError()
                except ValidationError as e:
                    logger.error("%s request invalid response: %s", request_name, e)
                    raise PositionsError()
                except requests.RequestException as e:
                    logger.error("%s request failed: %s", request_name, e)
                    raise PositionsError()

            return wrapper

        return decorator
  ```
- [ ] Implement comprehensive error logging for all documented exceptions