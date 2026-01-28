"""Mock LLM client for testing without real API credentials."""


class MockLLMClient:
    """Mock LLM client that generates realistic responses for testing."""

    def __init__(self):
        """Initialize mock LLM client."""
        self.name = "Mock LLM"

    def get_response(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 2000,
    ) -> str:
        """
        Generate a mock response based on user context.

        Args:
            system_prompt: System prompt for the model
            user_message: User message/query
            max_tokens: Maximum tokens in response

        Returns:
            Generated mock response text
        """
        # Extract user info from the message
        response = self._generate_upskilling_plan(user_message)
        return response

    def _generate_upskilling_plan(self, message: str) -> str:
        """Generate a realistic upskilling plan based on user profile."""
        # Parse the message for user info
        name = self._extract_field(message, "Name:")
        skills = self._extract_field(message, "Current Skills:")
        interests = self._extract_field(message, "Career Interests:")
        age = self._extract_field(message, "Age:")

        # Generate personalized response
        response = f"""**Personalized Upskilling Plan for {name}**

**Top 3 Skills to Learn Next:**
1. **Advanced Python/Data Engineering** - Builds on your technical foundation and aligns with high-demand roles
2. **Cloud Architecture (AWS/GCP)** - Critical for modern {interests} roles, especially in {interests}
3. **System Design & Scalability** - Essential for senior positions and architectural roles

**Recommended Learning Path:**

📅 **Short-term (0-3 months):**
- Complete a cloud certification course (AWS Solutions Architect Associate)
- Build 1-2 projects using cloud services relevant to {interests}
- Time commitment: 7-10 hours/week

📅 **Medium-term (3-6 months):**
- Deepen expertise in microservices and containerization (Docker, Kubernetes)
- Contribute to open-source projects in your area of interest
- Take advanced courses on system design
- Time commitment: 8-12 hours/week

📅 **Long-term (6-12 months):**
- Pursue role-based certifications (Cloud Architect, DevOps Engineer)
- Lead technical projects showcasing new skills
- Network with industry experts and mentors
- Time commitment: 5-8 hours/week

**Key Milestones:**
✓ Month 1-2: Foundation in cloud services
✓ Month 3: First cloud-based project
✓ Month 6: Cloud certification earned
✓ Month 12: Advanced project completion + mentoring others

**Resources:**
- Coursera, Udemy for structured learning
- LeetCode, HackerRank for practice
- GitHub for showcasing projects
- Local meetups and conferences for networking

This roadmap should help you advance toward your goals in {interests}. Start with foundation-building and progressively take on more complex projects!"""

        return response

    def _extract_field(self, message: str, field_name: str) -> str:
        """Extract a field value from the message."""
        try:
            if field_name in message:
                start = message.index(field_name) + len(field_name)
                end = message.index("\n", start) if "\n" in message[start:] else len(message)
                return message[start:end].strip().strip("-").strip()
        except (ValueError, IndexError):
            pass
        return "your field"
