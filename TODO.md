## Moving forward
- Implement trading package    
  - [ ] Implement working orders service
    - [x] Implement V2 GET /workingorders
      - [x] Implement v2 GET /workingorders response model
      - [x] Implement v2 GET /workingorders method
    - [x] Implement V2 POST /workingorders
      - [x] Implement v2 POST /workingorders/otc request model
      - [x] Implement v2 POST /workingorders/otc method
    - [ ] Implement V2 DELETE /workingorders
      - [ ] Implement V2 DELETE /workingorders/otc/{dealId} method
    - [ ] Implement V2 PUT /workingorders/otc/{dealId}
      - [ ] Implement V2 DELETE /workingorders/otc/{dealId} request model
      - [ ] Implement V2 DELETE /workingorders/otc/{dealId} method
  - [x] Implement positions service
    - [x] Implement V2 GET /positions
      - [x] Implement V2 GET /positions response model
      - [x] Implement V2 GET /positions method
    - [x] Implement V2 GET /positions/{dealId}
      - [x] Implement V2 GET /positions/{dealId} response model
      - [x] Implement V2 GET /positions/{dealId} method
    - [x] Implement V2 POST /positions
      - [x] Implement V2 POST /positions request model
      - [x] Implement V2 POST /positions method
    - [x] Implement V2 PUT /positions/{dealId}
      - [x] Implement V2 PUT /positions/{dealId} request model
      - [x] Implement V2 PUT /positions/{dealId} method
    - [x] Implement V2 DELETE /positions
      - [x] Implement V2 DELETE /positions/{dealId} method

- Implement Integration tests
  - [x] Implement authentication service tests
    - [x] Implement V2 POST /session tests 
  - [x] Implement positions service tests
    - [x] Implement V2 GET /positions tests
    - [x] Implement V2 GET /positions/{dealId} tests
    - [x] Implement V2 POST /positions tests
    - [x] Implement V2 PUT /positions/{dealId} tests
    - [x] Implement V2 DELETE /positions/{dealId} tests
  - [ ] Implement working orders service tests
    - [ ] Implement V2 GET /workingorders tests
    - [ ] Implement V2 POST /workingorders tests
    - [ ] Implement V2 DELETE /workingorders tests
    - [ ] Implement V2 PUT /workingorders/{dealId} tests

- Implement markets package
  - [ ] Implement markets service
    - [ ] Implement V1 GET /marketnavigation method
      - [ ] Implement V1 GET /marketnavigation response model
      - [ ] Implement V1 GET /marketnavigation method
    - [ ] Implement V1 GET /marketnavigation/{nodeId} method
      - [ ] Implement V1 GET /marketnavigation/{nodeId} response model
      - [ ] Implement V1 GET /marketnavigation/{nodeId} method 
    - [ ] Implement V1 GET /markets method
      - [ ] Implement V1 GET /markets request model
      - [ ] Implement V1 GET /markets response model
      - [ ] Implement V1 GET /markets method
    - [ ] Implement V1 GET /markets/{epic} method
      - [ ] Implement V1 GET /markets/{epic} response model
      - [ ] Implement V1 GET /markets/{epic} method
    - [ ] Implement V1 /markets?searchTerm={searchTerm} method
      - [ ] Implement V1 /markets?searchTerm={searchTerm} response model
      - [ ] Implement V1 /markets?searchTerm={searchTerm} method
  - [ ] Implement prices service
    - [ ] Implement V3 GET /prices/{epic} method
      - [ ] Implement V3 GET /prices/{epic} request model
      - [ ] Implement V3 GET /prices/{epic} response model
      - [ ] Implement V3 GET /prices/{epic} method

- Implement costs and charges package
  - [ ] Implement costs and charges service
    - [ ] Implement V1 POST /indicativecostsandcharges/open
      - [ ] Implement V1 POST /indicativecostsandcharges/open request model
      - [ ] Implement V1 POST /indicativecostsandcharges/open response model
      - [ ] Implement V1 POST /indicativecostsandcharges/open method
    - [ ] Implement V1 POST /indicativecostsandcharges/close
      - [ ] Implement V1 POST /indicativecostsandcharges/close request model
      - [ ] Implement V1 POST /indicativecostsandcharges/close response model
      - [ ] Implement V1 POST /indicativecostsandcharges/close method
    - [ ] Implement V1 POST /indicativecostsandcharges/edit
      - [ ] Implement V1 POST /indicativecostsandcharges/edit request model
      - [ ] Implement V1 POST /indicativecostsandcharges/edit response model
      - [ ] Implement V1 POST /indicativecostsandcharges/edit method


## Refinement
- [ ] Add a root module for field definitions
- [ ] Add a root module for validators
- [ ] Rename objects contains from plural to list. e.g. `OpenPositions` to `OpenPositionsList`
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