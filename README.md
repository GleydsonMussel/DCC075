# DCC075 Trabalho

## Montar Imagem
```console
docker build -t prison_break .
```

## Subir Container
```console
docker run -it --rm \
  --cap-drop=ALL \
  --security-opt no-new-privileges \
  prison_break
```

