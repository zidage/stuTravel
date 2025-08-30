# stuTravel

- A web application for scenic and campus tour planning, built with Vue 3 on the frontend and Java + SpringBoot on the backend.
- Parsed and cleaned map data for 144 public locations from OpenStreetMap, constructing a map database with over 13,000 Points of Interest (POIs), 1.3 million nodes, and 3.2 million paths.
- Optimized the cross-language system architecture using a thread pool and request queue mechanism, achieving an average core API response time of under 300ms.
- Designed a hybrid storage solution (MySQL for metadata, local files for spatial data), reducing database size by approximately 60% and improving query efficiency by 35%.
- Implemented the A* algorithm for millisecond-level pathfinding in large road networks and utilized the Christofides algorithm to provide near-optimal solutions for the Traveling Salesman Problem (TSP) with 50+ waypoints, processed in seconds.
