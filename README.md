Jenkins
=======
Jenkins playground.

Links:
- https://hub.docker.com/r/jenkins/jenkins
- https://github.com/jenkinsci/docker/blob/master/README.md
- https://plugins.jenkins.io

Change Log:
- https://www.jenkins.io/blog/2022/06/28/require-java-11/

Usage:
```bash
cd jenkins

podman-compose build
podman-compose up -d
podman-compose ps

# jenkins
127.0.0.1:8080
admin
admin

# secrets
127.0.0.1:8102
```

TODO:
- install job-builder plugin
- install version plugin https://plugins.jenkins.io/versioncolumn/
- kubernetes setup
- high availability
