# Generated by Django 5.1.5 on 2025-01-31 07:53

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trastorno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EvaluacionIA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo_ia', models.CharField(max_length=100)),
                ('puntuacion', models.FloatField()),
                ('diagnostico', models.CharField(max_length=100)),
                ('fecha_evaluacion', models.DateTimeField(auto_now_add=True)),
                ('trastorno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='core.trastorno')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('tipo', models.CharField(choices=[('usuario', 'Usuario'), ('psicologo', 'Psicólogo')], default='usuario', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, related_name='usuario_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='usuario_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_test', models.CharField(max_length=100)),
                ('fecha_realizacion', models.DateTimeField(auto_now_add=True)),
                ('puntuacion', models.IntegerField()),
                ('trastorno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='core.trastorno')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='core.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('leida', models.BooleanField(default=False)),
                ('tipo', models.CharField(choices=[('nuevo_paciente', 'Nuevo Paciente Asignado'), ('cita', 'Nueva Cita'), ('actualizacion', 'Actualización de Paciente'), ('nuevo_test', 'Nuevo Test Realizado'), ('nueva_recomendacion', 'Nueva Recomendación')], default='nuevo_paciente', max_length=50)),
                ('prioridad', models.CharField(choices=[('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')], default='media', max_length=10)),
                ('fecha_vencimiento', models.DateTimeField(blank=True, null=True)),
                ('psicologo', models.ForeignKey(limit_choices_to={'tipo': 'psicologo'}, on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones', to='core.usuario')),
            ],
            options={
                'ordering': ['-fecha_creacion'],
            },
        ),
        migrations.CreateModel(
            name='HistorialClinico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notas', models.TextField()),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('evaluaciones_ia', models.ManyToManyField(blank=True, related_name='historiales', to='core.evaluacionia')),
                ('psicologos', models.ManyToManyField(limit_choices_to={'tipo': 'psicologo'}, related_name='pacientes', to='core.usuario')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial', to='core.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='evaluacionia',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='core.usuario'),
        ),
        migrations.CreateModel(
            name='Conversacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje_usuario', models.TextField()),
                ('respuesta_chatbot', models.TextField()),
                ('estado_emocional', models.CharField(choices=[('neutral', 'Neutral'), ('triste', 'Triste'), ('ansioso', 'Ansioso'), ('feliz', 'Feliz')], default='neutral', max_length=50)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversaciones', to='core.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_cita', models.DateTimeField()),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('completada', 'Completada')], default='pendiente', max_length=20)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citas_paciente', to='core.usuario')),
                ('psicologo', models.ForeignKey(limit_choices_to={'tipo': 'psicologo'}, on_delete=django.db.models.deletion.CASCADE, related_name='citas_psicologo', to='core.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Recomendacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel_depresion', models.CharField(choices=[('leve', 'Leve'), ('moderado', 'Moderado'), ('severo', 'Severo')], max_length=10)),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('enlace', models.URLField()),
                ('trastorno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recomendaciones', to='core.trastorno')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recomendaciones', to='core.usuario')),
            ],
            options={
                'unique_together': {('usuario', 'trastorno', 'nivel_depresion')},
            },
        ),
    ]
