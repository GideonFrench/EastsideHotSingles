import matplotlib.pyplot as plt
import polars as pl
import seaborn as sns

# Prompt: what are five adjectives to describe Sarah?
poll = [
    ('H', 'kind,adventurous,caring,empathetic,sometimes anxious'), 
    ('M', 'smart,funny,sweet,cool,brave'), 
    ('E', 'creative,active,silly,persevering,smart'), 
    ('E', 'smart,kind,creative')
] #('C', ''),

poll_df = pl.DataFrame({'reviewer': [p[0] for p in poll], 'descriptors': [p[1] for p in poll]})

summary_df = (
    poll_df.with_columns(descriptors=pl.col('descriptors').str.split(','))
    .explode('descriptors')
    .group_by('descriptors')
    .agg(count=pl.len())
    .sort(['count', 'descriptors'], descending=True)
)

sns.barplot(data=summary_df.to_pandas(), x='count', y='descriptors', hue='descriptors')
plt.title(f'Descriptors of Sarah (n={len(poll)})')
plt.xlabel('Count')
plt.ylabel('Descriptor')
plt.tight_layout()
plt.savefig('sarah_descriptors.png', dpi=300)