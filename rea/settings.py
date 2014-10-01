from django.conf import settings


# Depending on the Economic system and the way the Domain Model
# has been created the Agent Models should be
# overridden to best describe the environment.
REA_RECEIVING_AGENT_MODEL = getattr(
    settings, 
    'REA_RECEIVING_AGENT_MODEL', 
    'rea.Agent'
)

REA_PROVIDING_AGENT_MODEL = getattr(
    settings, 
    'REA_PROVIDING_AGENT_MODEL', 
    'rea.Agent'
)

# Every REA Economic System is ultimately created from the 
# perspective of a primary reporting agent, usually the Enterprise
# using the system.
# 
# Givent the REA_PROVIDING_AGENT_MODEL, correlate the ID of that
# record that corresponds to this primary agent.
REA_REPORTING_AGENT_ID = getattr(
    settings, 
    'REA_REPORTING_AGENT_ID', 
    1
)

REA_REPORTING_AGENT_MODEL = getattr(
	settings,
	'REA_REPORTING_AGENT_MODEL',
	'rea.Agent'
)

# XXX include this later

# from django.db.models.loading import get_model

# from .settings import REA_PROVIDING_AGENT_MODEL, REA_REPORTING_AGENT_ID

# try:
#     AgentModel = get_model(*REA_PROVIDING_AGENT_MODEL.split('.',1))
#     AgentModel.objects.get(pk=REA_REPORTING_AGENT_ID)
# except AgentModel.DoesNotExist:
#     print "Warning your REA Primary Reporting Agent DoesNotExist"