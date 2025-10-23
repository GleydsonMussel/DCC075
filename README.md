# DCC075 Trabalho

## Montar Imagem
```console
docker build -t biohazard .
```

## Subir Container
```console
docker run -it --rm \
  --read-only \
  --tmpfs /tmp:rw,size=256m \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  -v $(pwd)/reports:/opt/analysis \
  biohazard

```

