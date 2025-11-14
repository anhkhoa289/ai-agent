"""Database management for storing sprint data, team metrics, and history."""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
import json


class Database:
    """Database manager for Scrum Master agent."""

    def __init__(self, db_url: str):
        """Initialize database connection."""
        # For simplicity, using SQLite. Can be extended to PostgreSQL, etc.
        self.db_path = db_url.replace("sqlite:///", "")
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Standup updates table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS standup_updates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    user_name TEXT NOT NULL,
                    yesterday TEXT,
                    today TEXT,
                    blockers TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Sprints table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sprints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id TEXT NOT NULL,
                    sprint_name TEXT NOT NULL,
                    start_date DATE,
                    end_date DATE,
                    goal TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # User stories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_stories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sprint_id INTEGER,
                    title TEXT NOT NULL,
                    description TEXT,
                    story_points INTEGER,
                    status TEXT DEFAULT 'backlog',
                    assignee_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sprint_id) REFERENCES sprints (id)
                )
            """)

            # Team velocity table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS team_velocity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id TEXT NOT NULL,
                    sprint_id INTEGER,
                    completed_points INTEGER,
                    committed_points INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sprint_id) REFERENCES sprints (id)
                )
            """)

            conn.commit()

    def save_standup_update(
        self,
        channel_id: str,
        user_id: str,
        user_name: str,
        yesterday: str,
        today: str,
        blockers: Optional[str] = None
    ):
        """Save a standup update."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO standup_updates (channel_id, user_id, user_name, yesterday, today, blockers)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (channel_id, user_id, user_name, yesterday, today, blockers))
            conn.commit()

    def get_recent_standups(self, channel_id: str, days: int = 1) -> List[Dict[str, Any]]:
        """Get recent standup updates."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_name, yesterday, today, blockers, created_at
                FROM standup_updates
                WHERE channel_id = ? AND created_at >= datetime('now', '-' || ? || ' days')
                ORDER BY created_at DESC
            """, (channel_id, days))

            rows = cursor.fetchall()
            return [
                {
                    "user_name": row[0],
                    "yesterday": row[1],
                    "today": row[2],
                    "blockers": row[3],
                    "created_at": row[4]
                }
                for row in rows
            ]

    def get_current_sprint(self, channel_id: str) -> Optional[Dict[str, Any]]:
        """Get the current active sprint."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, sprint_name, start_date, end_date, goal, status
                FROM sprints
                WHERE channel_id = ? AND status = 'active'
                ORDER BY created_at DESC
                LIMIT 1
            """, (channel_id,))

            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "start_date": row[2],
                    "end_date": row[3],
                    "goal": row[4],
                    "status": row[5]
                }
            return None

    def create_sprint(
        self,
        channel_id: str,
        sprint_name: str,
        start_date: str,
        end_date: str,
        goal: Optional[str] = None
    ) -> int:
        """Create a new sprint."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sprints (channel_id, sprint_name, start_date, end_date, goal)
                VALUES (?, ?, ?, ?, ?)
            """, (channel_id, sprint_name, start_date, end_date, goal))
            conn.commit()
            return cursor.lastrowid

    def get_team_velocity(self, channel_id: str, num_sprints: int = 3) -> Dict[str, Any]:
        """Calculate team velocity based on recent sprints."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    AVG(completed_points) as avg_completed,
                    AVG(committed_points) as avg_committed,
                    COUNT(*) as num_sprints
                FROM team_velocity tv
                JOIN sprints s ON tv.sprint_id = s.id
                WHERE s.channel_id = ?
                ORDER BY tv.created_at DESC
                LIMIT ?
            """, (channel_id, num_sprints))

            row = cursor.fetchone()
            if row and row[0]:
                return {
                    "average_velocity": round(row[0], 1),
                    "average_commitment": round(row[1], 1),
                    "sprints_analyzed": row[2]
                }
            return {
                "average_velocity": 0,
                "average_commitment": 0,
                "sprints_analyzed": 0
            }

    def add_user_story(
        self,
        sprint_id: Optional[int],
        title: str,
        description: Optional[str] = None,
        story_points: Optional[int] = None,
        assignee_id: Optional[str] = None
    ) -> int:
        """Add a user story."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_stories (sprint_id, title, description, story_points, assignee_id)
                VALUES (?, ?, ?, ?, ?)
            """, (sprint_id, title, description, story_points, assignee_id))
            conn.commit()
            return cursor.lastrowid

    def get_sprint_stories(self, sprint_id: int) -> List[Dict[str, Any]]:
        """Get all stories for a sprint."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, description, story_points, status, assignee_id
                FROM user_stories
                WHERE sprint_id = ?
                ORDER BY created_at
            """, (sprint_id,))

            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "story_points": row[3],
                    "status": row[4],
                    "assignee_id": row[5]
                }
                for row in rows
            ]
