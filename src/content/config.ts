import { defineCollection, z } from 'astro:content';

const CATEGORY_SLUGS = ['theory', 'cryptography', 'algorithm', 'os', 'unity', 'web-dev'] as const;

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    description: z.string().optional(),
    tags: z.array(z.string()).default([]),
    category: z.enum(CATEGORY_SLUGS).optional(),
    difficulty: z.enum(['입문', '중급', '심화']).optional(),
  }),
});

export const collections = { posts };
