import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const prerender = true;

export const GET: APIRoute = async () => {
  const posts = await getCollection('posts');
  const index = posts.map((post) => ({
    id: post.id,
    title: post.data.title,
    description: post.data.description ?? '',
    tags: post.data.tags ?? [],
    category: post.data.category ?? '',
  }));
  return new Response(JSON.stringify(index), {
    headers: { 'Content-Type': 'application/json' },
  });
};
