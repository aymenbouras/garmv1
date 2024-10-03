from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class StudentProgress(models.Model):
    user = models.ForeignKey(User, related_name='progress', on_delete=models.CASCADE)
    course = models.ForeignKey('CertificationCourse', related_name='progress', on_delete=models.CASCADE)

    # Chapitre et sous-chapitre courants
    current_chapter = models.ForeignKey('Chapter', related_name='current_chapter', on_delete=models.SET_NULL,
                                        blank=True, null=True)
    current_subchapter = models.ForeignKey('SubChapter', related_name='current_subchapter', on_delete=models.SET_NULL,
                                           blank=True, null=True)

    # Chapitres et sous-chapitres complétés
    completed_chapters = models.ManyToManyField('Chapter', related_name='completed_by', blank=True)
    completed_subchapters = models.ManyToManyField('SubChapter', related_name='completed_by', blank=True)

    # Suivi du temps passé par chapitre et sous-chapitre
    time_spent_per_chapter = models.JSONField(default=dict)  # Exemple : {"chapter_id": time_in_minutes}
    time_spent_per_subchapter = models.JSONField(default=dict)  # Exemple : {"subchapter_id": time_in_minutes}

    # Scores des quiz et tentatives
    quiz_scores = models.JSONField(default=dict)  # Exemple : {"quiz_id": {"score": 85, "attempts": 2}}
    total_quiz_score = models.FloatField(default=0)  # Score total accumulé pour le cours
    quiz_attempts = models.IntegerField(default=0)  # Nombre total de tentatives de quiz

    # Progression globale
    overall_progress = models.FloatField(default=0)  # Progression en pourcentage (par ex. 75%)

    # Certification
    is_certified = models.BooleanField(default=False)  # Indique si l'étudiant a obtenu la certification
    certification_attempts = models.IntegerField(default=0)  # Nombre de tentatives pour l'examen de certification
    certification_score_history = models.JSONField(
        default=dict)  # Historique des scores pour chaque tentative {"attempt_1": 85, "attempt_2": 90}

    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)  # Date de début du cours
    last_activity_at = models.DateTimeField(auto_now=True)  # Dernière activité de l'étudiant
    completed_at = models.DateTimeField(blank=True, null=True)  # Date à laquelle le cours a été complété

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    def calculate_overall_progress(self):
        """Calcule la progression globale de l'étudiant en pourcentage."""
        total_items = self.course.chapters.count() + \
                      self.course.chapters.aggregate(total_subchapters=models.Count('subchapters'))['total_subchapters']
        completed_items = self.completed_chapters.count() + self.completed_subchapters.count()
        if total_items > 0:
            self.overall_progress = (completed_items / total_items) * 100
        else:
            self.overall_progress = 0
        self.save()

    def update_quiz_score(self, quiz_id, score):
        """Met à jour le score d'un quiz et les tentatives de l'étudiant."""
        if quiz_id not in self.quiz_scores:
            self.quiz_scores[quiz_id] = {'score': score, 'attempts': 1}
        else:
            self.quiz_scores[quiz_id]['score'] = max(self.quiz_scores[quiz_id]['score'],
                                                     score)  # Conserve le meilleur score
            self.quiz_scores[quiz_id]['attempts'] += 1

        self.quiz_attempts += 1
        self.total_quiz_score = sum(quiz['score'] for quiz in self.quiz_scores.values()) / len(self.quiz_scores)
        self.save()

    def update_certification_score(self, score):
        """Met à jour l'historique des scores de certification."""
        self.certification_attempts += 1
        attempt_key = f"attempt_{self.certification_attempts}"
        self.certification_score_history[attempt_key] = score
        self.save()

    def mark_as_completed(self):
        """Marque le cours comme complété et attribue une date de complétion."""
        self.completed_at = timezone.now()
        self.is_certified = True
        self.save()

    def add_time_spent(self, chapter_id=None, subchapter_id=None, time_spent_minutes=0):
        """Ajoute du temps passé sur un chapitre ou sous-chapitre."""
        if chapter_id:
            self.time_spent_per_chapter[chapter_id] = self.time_spent_per_chapter.get(chapter_id,
                                                                                      0) + time_spent_minutes
        if subchapter_id:
            self.time_spent_per_subchapter[subchapter_id] = self.time_spent_per_subchapter.get(subchapter_id,
                                                                                               0) + time_spent_minutes
        self.save()
