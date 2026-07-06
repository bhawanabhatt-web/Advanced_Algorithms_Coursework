from __future__ import annotations
import sys
import threading
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1])) 
from Task2.graph import Graph  
from bfs_result import BFSResult  

__all__ = ["parallel_bfs"]


def parallel_bfs(graph: Graph, source: int, num_threads: int = 4) -> BFSResult:
    
    if not 0 <= source < graph.num_vertices:
        raise ValueError(f"Source vertex {source} is out of range.")
    if num_threads <= 0:
        raise ValueError(f"'num_threads' must be positive, got {num_threads}.")

    visited = [False] * graph.num_vertices
    visited[source] = True
    visit_order = [source]
    frontier = [source]
    lock = threading.Lock()

    while frontier:
        chunk_size = max(1, -(-len(frontier) // num_threads))  # ceil division
        chunks = [frontier[i:i + chunk_size] for i in range(0, len(frontier), chunk_size)]
        next_frontier_parts: list[list[int]] = [[] for _ in chunks]

        def worker(part_index: int, chunk: list[int]) -> None:
            """Process one chunk of the current frontier on a worker thread."""
            discovered: list[int] = []
            for vertex in chunk:
                for neighbour, _weight in graph.neighbors(vertex):
                    newly_discovered = False
                    with lock:  # --- critical section: check-and-set on `visited` ---
                        if not visited[neighbour]:
                            visited[neighbour] = True
                            newly_discovered = True
                    if newly_discovered:
                        discovered.append(neighbour)
            next_frontier_parts[part_index] = discovered

        threads = [
            threading.Thread(target=worker, args=(index, chunk))
            for index, chunk in enumerate(chunks)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        frontier = [vertex for part in next_frontier_parts for vertex in part]
        visit_order.extend(frontier)

    return BFSResult(source=source, visit_order=visit_order, visited=visited)