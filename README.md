# Game Description

The Viking Chess or simply Tafl is a two-player asymmetric strategy game. The defending side comprises 12 soldiers and a king, who start the game in a cross formation in the center of the board. The defending white army, surrounding the king try to defend him until the king is able to reach any of the four corners, while a larger black attacking army attempts to capture him. The attackers comprise 24 soldiers positioned in four groups of 6 around the perimeter of the board.

All pieces move like the Rook in chess and pieces are taken by sandwiching. Sandwiching means a piece is trapped horizontally or vertically between two attacking pieces. The playing grid layout is 9x9 or 11x11.

---

# Game Setup

- Initially, the King is placed on the central square (the Throne)
- 12 Defenders are placed around the King
- 24 Attackers are placed in four groups at the edges of the board

---

# How the game goes?

## Movement of Pieces
- All pieces (including the king) move any number of empty squares in a straight horizontal or vertical line ONLY (like a Rook in Chess)
- They cannot move off the edge of the board
- They cannot pass through other pieces
- A piece cannot share a space with another piece

## Capturing Opponents (Custodial Capture)
A piece is captured and removed from the board if it is "sandwiched" between two opposing pieces on opposite sides (horizontally or vertically). Other cases as below:

- You can remove an opponent’s piece if you capture it between the king’s throne and your piece; or between a corner space and your piece
- The king is unarmed; which means he cannot assist in capturing opponents
- Pieces may travel through a sandwich without being captured, but they may not stop inside a sandwich

## King's Escape
- The defenders win if the King reaches any of the four corner squares

## Capturing the KING
The attackers can win in the following cases:

- They surround the King on all four sides, preventing his movement
- If the king is against a wall, they can win by surrounding the other three sides
- If the king is against a corner, they can win by surrounding the other two sides

## Turn Order
- In Hnefatafl, the attacking player always moves first (one attacker per turn)
- After that, the turn goes to the defender (one defender per turn), and so on

# 🤖 AI Player (Alpha-Beta Algorithm)

The game includes an AI agent that uses the **Minimax algorithm with Alpha-Beta pruning** to make optimal decisions.

---

## 🧠 Overview

- The AI simulates future game states to choose the best possible move.
- It assumes:
  - The AI plays optimally
  - The opponent also plays optimally
- The algorithm explores a game tree of possible moves up to a certain depth.

---

## 🌳 Minimax Concept

- The game is modeled as a tree:
  - Each node represents a game state
  - Each edge represents a possible move

- Two types of players:
  - **Maximizing player** → tries to maximize the score (AI)
  - **Minimizing player** → tries to minimize the score (opponent)

---

## ✂️ Alpha-Beta Pruning

Alpha-Beta pruning improves Minimax by **eliminating branches that will not affect the final decision**.

- **Alpha (α):** Best value the maximizer can guarantee so far
- **Beta (β):** Best value the minimizer can guarantee so far

### Pruning Condition
- If `β ≤ α`, the branch is pruned (ignored)

This significantly reduces:
- Number of explored nodes
- Execution time

---

## ⚙️ Evaluation Function

The AI evaluates board states using a heuristic function that considers:

- Distance of the King to the nearest corner
- Number of remaining defenders and attackers
- King safety (surrounded sides)
- Control of key positions (center, paths to corners)

The evaluation returns:
- Positive score → favorable for AI
- Negative score → unfavorable for AI

---

## 🔄 Algorithm Flow

1. Generate all valid moves
2. Apply each move to create new states
3. Recursively evaluate states using Minimax
4. Apply Alpha-Beta pruning to skip unnecessary branches
5. Select the move with the best evaluation score

---

## ⚡ Performance Notes

- Alpha-Beta pruning greatly reduces computation compared to plain Minimax
- Depth limit is used to control execution time
- Move ordering can further improve pruning efficiency

---

## 🧩 Integration

- The AI can play as:
  - Attacker
  - Defender
- It is integrated with the game controller:
  - Receives current board state
  - Returns the best move
