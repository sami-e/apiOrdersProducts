import subprocess as sp

result = sp.run("docker container stop projet-de-session-ocean_db_1; "
                "docker container stop projet-de-session-ocean_cache_1; "
                "docker container prune; docker volume prune; docker-compose up -d", shell=True)
