# Dados Brutos — TweetSentBR

Este diretório é reservado para o dataset base utilizado no benchmark zero-shot.

## Download

O **TweetSentBR** está disponível publicamente no Hugging Face Hub:

🔗 https://huggingface.co/datasets/pysentimiento/tweetsentbr

### Via Python (recomendado)

```python
from datasets import load_dataset

ds = load_dataset("pysentimiento/tweetsentbr")
```

### Via CLI

```bash
pip install datasets
python -c "from datasets import load_dataset; load_dataset('pysentimiento/tweetsentbr')"
```

O dataset será baixado automaticamente para o cache do Hugging Face (`~/.cache/huggingface/`).  
Se preferir salvar localmente nesta pasta:

```python
ds = load_dataset("pysentimiento/tweetsentbr")
ds.save_to_disk("data/raw/tweetsentbr")
```

> ⚠️ O dataset original **não está incluído neste repositório** por licença e tamanho.  
> Consulte os termos de uso em: https://huggingface.co/datasets/pysentimiento/tweetsentbr
