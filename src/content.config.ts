import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const CATEGORY_SLUGS = ['theory', 'cryptography', 'algorithm', 'os', 'unity', 'web-dev'] as const;

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    description: z.string().optional(),
    tags: z.array(z.string()).default([]),
    category: z.enum(CATEGORY_SLUGS).optional(),
  }),
});

export const collections = { posts };
