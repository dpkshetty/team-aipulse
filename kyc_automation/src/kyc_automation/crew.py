from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from kyc_automation.tools.custom_tool import MySQLQueryTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

llm = LLM(
    model="<your-model-name>",
    base_url="<model-base-url>",
    api_key="<api-key>"
)

@CrewBase
class KycAutomation():
	"""KycAutomation crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def db_developer(self) -> Agent:
		return Agent(
			config=self.agents_config['db_developer'],
			llm=llm
		)

	@agent
	def SQL_Sentinel(self) -> Agent:
		return Agent(
			config=self.agents_config['SQL_Sentinel'],
			llm=llm,
			tools=[MySQLQueryTool()],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def createSQL(self) -> Task:
		return Task(
			config=self.tasks_config['createSQL'],
		)

	@task
	def queryDB(self) -> Task:
		return Task(
			config=self.tasks_config['queryDB'],
			context=[self.createSQL()]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the KycAutomation crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
