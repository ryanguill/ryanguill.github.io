---
layout: post
title:  "Optimizing Search with Parallel Queries in TypeScript"
date:   2024-10-19 15:00:00
author: Ryan Guill
categories: typescript js
tags:	typescript javascript js promise
---
Recently, I encountered a situation where I built a search interface for a backend process. Users could search using various criteria—different identifiers or other metadata tagged to the records. However, the query I initially wrote to handle these searches didn't perform well. It relied heavily on `OR` conditions or `IN` clauses (which are logically equivalent to `OR`), making indexing difficult and query performance sluggish<sup>[1]</sup>

In this case, all the different search options were mutually exclusive — if results were found using one criterion, no other criterion would yield results. All our identifiers are UUIDs or globally unique formats, ensuring that only one search method could return valid results. Additionally, some queries were fast and efficient, while others were slower and more resource-intensive. Combining all these into a single query meant the user would always have to wait for the slowest part of the search, even if they were searching for something could return results immediately.

## A Different Approach: Parallel Query Execution

To improve performance, I decided to run multiple searches in parallel and return results as soon as one of them succeeded. If none of the queries returned results, the system would fall back to showing the latest records. This solution is somewhat similar to [Promise.race()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/race), but with a twist. `Promise.race()` resolves or rejects with the first settled promise, regardless of whether it yields useful data. In my case, I wanted to inspect the resolved values and only return a result if it contained results.

After working with ChatGPT, Claude, and some friends, I developed the following solution. Below are two versions of the function—one that uses key-value pairs for better traceability and another that works with an array of queries. I have more to say about it below.

## Implementation

```typescript
/**
 * Runs multiple queries in parallel and resolves with the first query that returns records.
 * If no query returns records, it rejects with an error.
 *
 * @param queries An array of promises representing database queries.
 * @returns A promise that resolves with the first valid result or rejects if no results are found.
 */
export async function firstQueryWithResultsWithKey<T>({
  queriesAsRecord,
  resultTest = ({ result }) => Array.isArray(result) && result.length > 0,
  noResultsReturn = null,
}: {
  queriesAsRecord: Record<string, Promise<T>>;
  resultTest?: ({ result, key }: { result: T; key: string | null }) => boolean;
  noResultsReturn?: T | null;
}): Promise<{ result: T; key: string | null }> {
  return new Promise((resolve, reject) => {
    let completed = false; // Track if a query has returned results
    let pendingCount = Object.keys(queriesAsRecord).length; // Track the number of pending queries

    if (pendingCount === 0) {
      if (noResultsReturn) {
        resolve({ result: noResultsReturn, key: null });
      } else {
        reject(new Error("No queries returned any records"));
      }
    }

    // Define a function to handle each query independently
    const handleQuery = async (query: Promise<T>, key: string) => {
      try {
        if (!completed) {
          const result = await query;

          // If the result has records and no other query has resolved
          if (resultTest({ result, key }) && !completed) {
            completed = true; 
            resolve({ result, key }); // Resolve with the first valid result
          }
        }
      } catch (error) {
        console.error("Query error:", error); // Log query errors
      } finally {
        // Decrement pending count and check if all queries are exhausted
        pendingCount--;
        if (pendingCount === 0 && !completed) {
          if (noResultsReturn) {
            resolve({ result: noResultsReturn, key: null });
          } else {
            reject(new Error("No queries returned any records"));
          }
        }
      }
    };

    // Start all queries in parallel
    Object.entries(queriesAsRecord).forEach(([key, query]) =>
      handleQuery(query, key),
    );
  });
}

export async function firstQueryWithResults<T>({
  queries,
  resultTest = (result) => Array.isArray(result) && result.length > 0,
  noResultsReturn = null,
}: {
  queries: Promise<T>[];
  resultTest?: (result: T) => boolean;
  noResultsReturn?: T | null;
}): Promise<T> {
  let queriesAsRecord = Object.fromEntries(
    queries.map((query, index) => [index.toString(), query]),
  );

  const { result } = await firstQueryWithResultsWithKey({
    queriesAsRecord,
    resultTest: ({ result }) => resultTest(result),
    noResultsReturn,
  });
  return result;
}

```

Both versions of the function execute a collection of promises in parallel, returning the first valid result. If no queries pass the `resultTest`, the function returns the provided fallback value (if any) or throws an error.

## Example Usage

Here’s a unit test to demonstrate how the function works:

```typescript
const wait = (interval: number) =>
    new Promise((resolve) => setTimeout(resolve, interval));

it("should return the noResultsReturn value if no queries return results", async () => {
    const query1 = async ({ id }: { id: string }): Promise<QueryResult> => {
      await wait(100);
      return [];
    };
    const query2 = async ({ id }: { id: string }): Promise<QueryResult> => {
      await wait(200);
      return [];
    };
    const query3 = async ({ id }: { id: string }): Promise<QueryResult> => {
      await wait(300);
      return [{a: id}];
    };

    let result: QueryResult | null = null;

    result = await firstQueryWithResults({
      queries: [query1({ id: "1" }), query2({ id: "2" }), query3({ id: "3" })],
      resultTest: (result) => result.length > 0,
      noResultsReturn: [],
    });
    expect(result).toEqual([]);
  });

```

In this test, three promises simulate query operations. The first two return empty arrays after 100ms and 200ms, while the third returns a valid result after 300ms. The `resultTest` function ensures that only non-empty arrays pass the validation.

<hr />

## Reflections and Considerations

This approach improves user experience by returning results as quickly as possible, but it also increases the load on the database since multiple queries run in parallel. For my use case — an internal back-office tool — I find the trade-off acceptable. However, I plan to monitor system performance to ensure this doesn't impact the overall system.

An alternative approach would be to let users specify the type of identifier they are searching for. This way, the system would only execute the relevant query, reducing database load. However, the current solution offers a seamless experience since users don't need to know or care about the type of identifier—they just paste it and search.

Although I used the term "query" throughout the article because of my use case, the function is generic and can be applied to any collection of promises, not just database operations.

I welcome any feedback or suggestions on this approach. While I'm not fully convinced this is the optimal solution, I found the challenge of reimagining `Promise.race()` to be an interesting exercise.

Here is a gist with the function and more unit tests so you can see how it works: [https://gist.github.com/ryanguill/e89931f9d223e74dabcb070879a58298](https://gist.github.com/ryanguill/e89931f9d223e74dabcb070879a58298)


[1] There are ongoing improvements in PostgreSQL to optimize queries with OR conditions. For more, see: [https://www.crunchydata.com/blog/real-world-performance-gains-with-postgres-17-btree-bulk-scans](https://www.crunchydata.com/blog/real-world-performance-gains-with-postgres-17-btree-bulk-scans)
