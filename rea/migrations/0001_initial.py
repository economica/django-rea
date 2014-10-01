# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import entropy.base
from django.conf import settings
import django.db.models.base
from django_xworkflows import models as xwf_models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('short_title', models.CharField(max_length=255, blank=True)),
                ('slug', models.SlugField(max_length=255)),
                ('polymorphic_ctype', models.ForeignKey(related_name=b'polymorphic_rea.agent_set', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(entropy.base.BaseSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Clause',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(default=b'', blank=True)),
                ('title', models.CharField(max_length=255)),
                ('short_title', models.CharField(max_length=255, blank=True)),
                ('polymorphic_ctype', models.ForeignKey(related_name=b'polymorphic_rea.clause_set', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClauseRuleAspect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Commitment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('occured_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_terminated', models.BooleanField(default=False)),
                ('polymorphic_ctype', models.ForeignKey(related_name=b'polymorphic_rea.contract_set', editable=False, to='contenttypes.ContentType', null=True)),
                ('providing_agent', models.ForeignKey(related_name=b'rea_contract_providing_agent', to='rea.Agent')),
                ('receiving_agent', models.ForeignKey(related_name=b'rea_contract_receiving_agent', to='rea.Agent')),
            ],
            options={
                'abstract': False,
            },
            bases=(xwf_models.WorkflowEnabled, models.Model),
        ),
        migrations.CreateModel(
            name='ContractClause',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0, blank=True)),
                ('clause', models.ForeignKey(to='rea.Clause')),
                ('contract', models.ForeignKey(to='rea.Contract')),
                ('polymorphic_ctype', models.ForeignKey(related_name=b'polymorphic_rea.contractclause_set', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContractInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContractInstanceClause',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0, blank=True)),
                ('clause', models.ForeignKey(to='rea.Clause')),
                ('contract_instance', models.ForeignKey(to='rea.ContractInstance')),
                ('polymorphic_ctype', models.ForeignKey(related_name=b'polymorphic_rea.contractinstanceclause_set', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContractTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('short_title', models.CharField(max_length=255, blank=True)),
                ('polymorphic_ctype', models.ForeignKey(related_name=b'polymorphic_rea.contracttemplate_set', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DecrementCommitmentLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField()),
                ('recieving_agent', models.ForeignKey(related_name=b'rea_decrementcommitmentline_recieving_agents', to='rea.Agent')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('occured_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DecrementEvent',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.Event')),
                ('quantity', models.FloatField()),
                ('recieving_agent', models.ForeignKey(related_name=b'rea_decrementevent_recieving_agents', to='rea.Agent')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.event', models.Model),
        ),
        migrations.CreateModel(
            name='FulfilmentMade',
            fields=[
                ('clauseruleaspect_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.ClauseRuleAspect')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.clauseruleaspect',),
        ),
        migrations.CreateModel(
            name='IncrementCommitmentLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField()),
                ('providing_agent', models.ForeignKey(related_name=b'rea_incrementcommitmentline_providing_agents', to='rea.Agent')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IncrementEvent',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.Event')),
                ('quantity', models.FloatField()),
                ('providing_agent', models.ForeignKey(related_name=b'rea_incrementevent_providing_agents', to='rea.Agent')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.event', models.Model),
        ),
        migrations.CreateModel(
            name='PaymentReceived',
            fields=[
                ('clauseruleaspect_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rea.ClauseRuleAspect')),
            ],
            options={
                'abstract': False,
            },
            bases=('rea.clauseruleaspect',),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('polymorphic_ctype', models.ForeignKey(related_name=b'polymorphic_rea.resource_set', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='incrementevent',
            name='resource',
            field=models.ForeignKey(to='rea.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incrementcommitmentline',
            name='resource',
            field=models.ForeignKey(to='rea.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='commitment',
            field=models.ForeignKey(related_name=b'rea_event_commitment', to='rea.Commitment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name=b'polymorphic_rea.event_set', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='decrementevent',
            name='resource',
            field=models.ForeignKey(to='rea.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='decrementcommitmentline',
            name='resource',
            field=models.ForeignKey(to='rea.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commitment',
            name='contract',
            field=models.ForeignKey(to='rea.Contract'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commitment',
            name='decrement_line',
            field=models.ForeignKey(related_name=b'rea_commitment_decrement_commitment_lines', to='rea.DecrementCommitmentLine'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commitment',
            name='increment_line',
            field=models.ForeignKey(related_name=b'rea_commitment_increment_commitment_lines', to='rea.IncrementCommitmentLine'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clauseruleaspect',
            name='created_by',
            field=models.ForeignKey(related_name=b'rea_clauseruleaspect_created_by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clauseruleaspect',
            name='modified_by',
            field=models.ForeignKey(related_name=b'rea_clauseruleaspect_modified_by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clauseruleaspect',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name=b'polymorphic_rea.clauseruleaspect_set', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
    ]
